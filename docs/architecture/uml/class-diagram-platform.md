# Class Diagram — AegisSRE Platform

> **Diagram 2a (UML 2.5 — Structural).** Static structure of the AegisSRE platform:
> all layers — telemetry envelope, event layer, core domain (services, incidents,
> remediation, policy, audit), ML detection, and AI reasoning/RAG/tools.
> Full detail: attributes with types, methods, multiplicity, inheritance,
> composition/aggregation, and interface realization. Decided 2026-08-31.

```mermaid
classDiagram
    direction LR

    %% ═══════════════════════════════════════════════════════
    %% LAYER 1 — TELEMETRY & EVENT ENVELOPE (telemetry-model.md)
    %% ═══════════════════════════════════════════════════════
    class EventEnvelope {
        +str id
        +str schema_version
        +datetime timestamp
        +str source
        +str type
        +str service
        +str environment
        +str correlation_id
        +str trace_id
        +str severity
        +DeploymentContext deployment
        +dict payload
        +validate() bool
        +to_json() str
    }
    class DeploymentContext {
        +str revision
        +str version
        +datetime changed_at
    }
    class MetricEvent {
        +str name
        +dict labels
        +float value
        +str unit
    }
    class AnomalyEvent {
        +float score
        +float threshold
        +str model
        +Window window
        +Baseline baseline
    }
    class DeploymentEvent {
        +str action
        +str revision
        +str previous_revision
        +str triggered_by
        +str status
    }

    EventEnvelope --> DeploymentContext : references
    MetricEvent <|-- EventEnvelope
    AnomalyEvent <|-- EventEnvelope
    DeploymentEvent <|-- EventEnvelope

    %% ═══════════════════════════════════════════════════════
    %% LAYER 2 — EVENT LAYER (Redis Streams, ADR-0004)
    %% ═══════════════════════════════════════════════════════
    class EventBus {
        <<interface>>
        +publish(envelope) void
        +subscribe(consumer) void
    }
    class RedisEventBus {
        -RedisClient redis
        -dict~str, int~ stream_ttls
        +publish(envelope) void
        +subscribe(consumer) void
        +ack(stream, id) void
    }
    class EventConsumer {
        <<interface>>
        +consume() void
    }

    RedisEventBus ..|> EventBus
    EventConsumer ..|> EventBus

    %% ═══════════════════════════════════════════════════════
    %% LAYER 3 — CORE DOMAIN (backend services)
    %% ═══════════════════════════════════════════════════════
    class Service {
        +str id
        +str name
        +str owner
        +str environment
        +str health
        +list~SLO~ slos
        +register() void
        +update_health(status) void
        +get_health() str
    }
    class SLO {
        +str name
        +float target
        +float budget_remaining
        +str window
        +calculate_burn_rate() float
    }
    class Incident {
        +str id
        +IncidentStatus status
        +int severity
        +datetime created_at
        +datetime detected_at
        +datetime resolved_at
        +list~str~ affected_service_ids
        +list~Anomaly~ anomalies
        +list~Evidence~ evidence
        +list~TimelineEvent~ timeline
        +RootCauseHypothesis root_cause
        +create(anomalies) Incident
        +transition(status) void
        +attach_evidence(evidence) void
        +close() void
        +escalate() void
        +mttd() float
        +mttr() float
    }
    class IncidentStatus {
        <<enum>>
        OPEN
        INVESTIGATING
        REMEDIATING
        VERIFYING
        CLOSED
        ESCALATED
    }
    class TimelineEvent {
        +datetime ts
        +str type
        +str description
        +dict metadata
    }
    class Evidence {
        +str id
        +str type
        +str source
        +dict content
        +str trace_id
        +datetime captured_at
    }
    class Anomaly {
        +str id
        +str metric
        +dict labels
        +float score
        +float threshold
        +str model
        +Window window
        +Baseline baseline
    }
    class Window {
        +datetime start
        +datetime end
    }
    class Baseline {
        +float mean
        +float std
    }
    class RemediationAction {
        +str id
        +str incident_id
        +ActionType action_type
        +RiskClass risk_class
        +str mode
        +str status
        +str approved_by
        +ExecutionRecord execution
        +recommend() void
        +approve(user) void
        +reject(user, reason) void
        +execute() void
        +cancel() void
    }
    class ActionType {
        <<enum>>
        RESTART
        ROLLBACK
        SCALE
        REPLACE_INSTANCE
        CONFIG_UPDATE
        ESCALATE
    }
    class RiskClass {
        <<enum>>
        LOW
        MEDIUM
        HIGH
        FORBIDDEN
    }
    class ExecutionRecord {
        +str command
        +str result
        +datetime started_at
        +datetime finished_at
    }
    class Policy {
        +str id
        +list~str~ actions
        +RiskClass risk_class
        +bool reversible
        +bool requires_approval
        +int max_blast_radius
        +str cooldown
        +list~PolicyCondition~ conditions
        +evaluate(context) Decision
    }
    class PolicyCondition {
        +str field
        +str operator
        +float value
    }
    class Decision {
        +str mode
        +str reason
    }
    class ApprovalRequest {
        +str id
        +str action_id
        +str requested_by
        +str approved_by
        +str status
        +str reason
        +approve(user) void
        +reject(user, reason) void
        +defer(user, reason) void
    }
    class AuditLogEntry {
        +str id
        +datetime ts
        +str actor
        +str action
        +str target
        +str outcome
        +str reason
    }
    class AutonomyController {
        -AutonomyMode mode
        +set_mode(mode) void
        +current_mode() AutonomyMode
    }
    class AutonomyMode {
        <<enum>>
        OBSERVE
        RECOMMEND
        APPROVAL
        SAFE_AUTO
    }

    %% ── Domain relationships ──────────────────────────────
    Service "1" --> "0..*" Incident : affects
    Service "1" o-- "1..*" SLO
    Incident "1" --> "1" IncidentStatus
    Incident "1" *-- "0..*" Evidence
    Incident "1" *-- "0..*" TimelineEvent
    Incident "1" o-- "0..*" Anomaly : caused by
    Incident "1" --> "0..1" RootCauseHypothesis
    Incident "1" --> "0..*" RemediationAction
    Anomaly "1" --> "1" Window
    Anomaly "1" --> "1" Baseline
    RemediationAction "1" --> "1" ActionType
    RemediationAction "1" --> "1" RiskClass
    RemediationAction "1" --> "1" Policy : evaluated by
    RemediationAction "1" --> "0..1" ExecutionRecord
    RemediationAction ..> AuditLogEntry : logged
    ApprovalRequest "1" --> "1" RemediationAction
    ApprovalRequest ..> AuditLogEntry : logged
    Policy "1" *-- "1..*" PolicyCondition
    Policy "1" --> "1" Decision : yields
    AutonomyController "1" --> "1" AutonomyMode

    %% ═══════════════════════════════════════════════════════
    %% LAYER 4 — ML ANOMALY DETECTION (ml/)
    %% ═══════════════════════════════════════════════════════
    class AnomalyDetector {
        <<abstract>>
        +score(series) float
        +detect(series) list~Anomaly~
    }
    class StatisticalDetector {
        -float z_threshold
        -float ewma_alpha
        +score(series) float
        +detect(series) list~Anomaly~
    }
    class IsolationForestDetector {
        -object model
        -float contamination
        +train(samples) void
        +score(series) float
        +detect(series) list~Anomaly~
    }
    class FeaturePipeline {
        +extract(raw) dataframe
        +rolling_window(series, n) series
        +residual(series) series
    }
    class AnomalyService {
        -list~AnomalyDetector~ detectors
        -EventBus bus
        +evaluate(service, metric) list~Anomaly~
        +publish(anomaly) void
    }

    StatisticalDetector <|-- AnomalyDetector
    IsolationForestDetector <|-- AnomalyDetector
    AnomalyService "1" o-- "1..*" AnomalyDetector
    AnomalyService --> FeaturePipeline
    AnomalyService --> EventBus : publishes
    AnomalyService ..> AnomalyEvent : emits

    %% ═══════════════════════════════════════════════════════
    %% LAYER 5 — AI REASONING, RAG & TOOLS (ai/)
    %% ═══════════════════════════════════════════════════════
    class ReasoningEngine {
        -LLMClient llm
        -list~Tool~ tools
        -RAGRetriever retriever
        +collect_evidence(incident) list~Evidence~
        +generate_hypotheses(incident) list~RootCauseHypothesis~
        +recommend_remediation(hypothesis) list~RemediationAction~
    }
    class RootCauseHypothesis {
        +str summary
        +float confidence
        +list~Evidence~ evidence
        +str failure_pattern
        +str runbook_id
    }
    class Tool {
        <<interface>>
        +name() str
        +description() str
        +invoke(params) dict
    }
    class GetMetricsTool {
        -MetricsClient client
        +name() str
        +invoke(params) dict
    }
    class GetLogsTool {
        -LogsClient client
        +name() str
        +invoke(params) dict
    }
    class GetTracesTool {
        -TracesClient client
        +name() str
        +invoke(params) dict
    }
    class GetServiceHealthTool {
        -RegistryClient client
        +name() str
        +invoke(params) dict
    }
    class GetDeploymentHistoryTool {
        -DeploymentsClient client
        +name() str
        +invoke(params) dict
    }
    class GetKubernetesEventsTool {
        -K8sClient client
        +name() str
        +invoke(params) dict
    }
    class GetRunbookTool {
        -RAGRetriever retriever
        +name() str
        +invoke(params) dict
    }
    class RAGRetriever {
        -VectorStore store
        -Embedder embedder
        +embed(text) vector
        +retrieve(query, top_k) list~Document~
    }
    class Document {
        +str id
        +str content
        +str source
        +float score
    }
    class AskAegisService {
        -ReasoningEngine engine
        -list~Tool~ tools
        +answer(question) Answer
    }
    class Answer {
        +str text
        +list~ToolCall~ calls
        +list~Evidence~ citations
    }
    class ToolCall {
        +str tool_name
        +dict params
        +dict result
    }
    class PostmortemGenerator {
        -LLMClient llm
        +generate(incident) str
    }

    ReasoningEngine "1" o-- "0..*" Tool
    ReasoningEngine --> RAGRetriever
    RAGRetriever "1" --> "0..*" Document
    GetMetricsTool ..|> Tool
    GetLogsTool ..|> Tool
    GetTracesTool ..|> Tool
    GetServiceHealthTool ..|> Tool
    GetDeploymentHistoryTool ..|> Tool
    GetKubernetesEventsTool ..|> Tool
    GetRunbookTool ..|> Tool
    AskAegisService "1" o-- "0..*" Tool
    AskAegisService --> ReasoningEngine
    Answer "1" o-- "0..*" ToolCall
    Answer "1" o-- "0..*" Evidence
    PostmortemGenerator --> Incident
    ReasoningEngine ..> AuditLogEntry : logged

    %% ═══════════════════════════════════════════════════════
    %% LAYER COLOR CODING (legend below)
    %% ═══════════════════════════════════════════════════════
    classDef telemetry fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef eventlayer fill:#ede9fe,stroke:#7c3aed,color:#4c1d95;
    classDef domain fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ml fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    class EventEnvelope,DeploymentContext,MetricEvent,AnomalyEvent,DeploymentEvent telemetry;
    class EventBus,RedisEventBus,EventConsumer eventlayer;
    class Service,SLO,Incident,IncidentStatus,TimelineEvent,Evidence,Anomaly,Window,Baseline,RemediationAction,ActionType,RiskClass,ExecutionRecord,Policy,PolicyCondition,Decision,ApprovalRequest,AuditLogEntry,AutonomyController,AutonomyMode domain;
    class AnomalyDetector,StatisticalDetector,IsolationForestDetector,FeaturePipeline,AnomalyService ml;
    class ReasoningEngine,RootCauseHypothesis,Tool,GetMetricsTool,GetLogsTool,GetTracesTool,GetServiceHealthTool,GetDeploymentHistoryTool,GetKubernetesEventsTool,GetRunbookTool,RAGRetriever,Document,AskAegisService,Answer,ToolCall,PostmortemGenerator ai;
```

---

## 1. Purpose

Static model of the platform's classes, organized in five layers. This is the
implementation blueprint for the backend (Jegatheesan), ML (Navin), AI (Navin), and
event layer (Gokul/Navin) — every class maps to a feature in `features.md`.

## 2. Layer Legend

| Color | Layer | Package (planned) | Owned by |
|---|---|---|---|
| 🔵 Blue | Telemetry & Envelope | `backend/libs/telemetry` | Navin (design) |
| 🟣 Purple | Event Layer | `backend/libs/eventbus` | Navin + Gokul |
| 🟢 Green | Core Domain | `backend/services/*` | Jegatheesan (impl), Navin (design) |
| 🟠 Orange | ML Detection | `ml/` | Navin |
| 🩷 Pink | AI Reasoning / RAG / Tools | `ai/` | Navin |

## 3. Key Relationship Semantics

| Relationship | Meaning |
|---|---|
| `Incident *-- Evidence` | Composition: evidence belongs to exactly one incident (append-only) |
| `Incident o-- Anomaly` | Aggregation: anomalies exist independently (from the ML layer) |
| `Service "1" --> "0..*" Incident` | One service can be affected by many incidents |
| `RemediationAction --> Policy` | Every action is evaluated by exactly one policy (policy engine is the only decision point) |
| `* ..|> Tool` | Tool realization — the seven read-only tools the AI may invoke (no write tools exist) |
| `AnomalyService ..> AnomalyEvent` | ML emits anomaly events onto the event bus (decoupled from the incident manager) |
| `StatisticalDetector <|-- AnomalyDetector` | Abstract detector; two concrete strategies (strategy pattern) |

## 4. Notes for Implementers

- Nullability (e.g., `root_cause` may be absent) is modeled via `0..1` multiplicity, not types.
- Enum classes become Python `enum.Enum` / database check constraints.
- The `Tool` interface is the **security boundary**: only these seven tools are compiled into the runtime — the AI cannot invent new tools (autonomy-model.md §3).
- Full attribute/method lists here are the contract; deviations need a PR + ADR note.
