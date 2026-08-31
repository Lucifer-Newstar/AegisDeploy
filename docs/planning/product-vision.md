# Product Vision

> How the final AegisSRE product should look and behave. This is the target for the
> frontend (Dhanush) and the contract for what the backend/AI must expose. Decided
> 2026-08-31; visual details are refined with Member 1 during design, but the
> concepts below are locked.

---

## 1. One-Liner

> **AegisSRE Console** — the AI-powered SRE control plane: *observe everything,
> trust evidence, reason over context, act within boundaries, verify the result.*

## 2. Who It Is For

A single SRE / DevOps engineer (or a small on-call team) responsible for one
cloud-native application. The console is their **single pane of glass** for the
whole incident lifecycle — and their **governance point** when the platform wants to
act.

## 3. Design Language

| Element | Decision |
|---|---|
| Theme | Dark, observability aesthetic (Grafana/Datadog family). Dense but readable; data-first. |
| Layout | Left sidebar navigation; top status bar with **system health** and **autonomy mode** (OBSERVE / RECOMMEND / APPROVAL / SAFE-AUTO); main content area. |
| Severity colors | sev1 red · sev2 orange · sev3 amber · sev4 blue (consistent everywhere: badges, charts, timeline). |
| AI content marking | Every AI-generated element carries an **"AI · evidence-cited" badge**; nothing AI-written looks like ground truth. |
| Evidence | Every AI claim is a clickable card linking to the raw telemetry (Prometheus query, Loki log line, Tempo trace, k8s event). |
| Status | Incident states use the canonical state machine: open → investigating → remediating → verifying → closed/escalated. |

## 4. Pages (7)

### 4.1 Command Center (overview)
- Service health grid (live, from A2)
- Live incident feed (newest first, severity-colored)
- Anomaly sparklines per service (last 24 h)
- Stat cards: **MTTD, MTTR**, open incidents, autonomy mode
- One-click "Ask Aegis" entry point

### 4.2 Service Detail
- Metric charts with **anomaly windows shaded red**
- Logs tab (LogQL), Traces tab (Tempo), Deployments tab (history), Incidents tab (this service)
- SLO panel with budget remaining + burn rate

### 4.3 Incident Detail — *the hero screen*
- **Header:** severity badge, status, affected services, MTTD/MTTR timers, autonomy level
- **Left column:** vertical incident timeline (anomaly → evidence → RCA → recommendation → action → verification → close)
- **Right column (AI Reasoning panel):** root-cause hypotheses with confidence bars and **evidence cards** (source icon: Prometheus / Loki / Tempo / k8s / deployment)
- **Below:** telemetry charts with anomaly bands; raw evidence expandable
- **Action panel:** recommended remediation, risk badge, impact summary, Approve / Reject / Defer (or "auto-executed" stamp + result)

### 4.4 Approvals Queue
- Pending actions with risk badges (low/medium/high)
- Impact summary per action ("restart 1 of 3 replicas, ~5 s blip, reversible")
- Approve / Reject / Defer with optional reason; audit stamp on every action

### 4.5 Postmortem
- Rendered AI report: timeline, evidence, actions taken, metrics (MTTD/MTTR), lessons, action items
- Exportable (markdown/PDF) — thesis appendix material

### 4.6 Runbooks
- Markdown runbook list + viewer; linked from incidents ("Runbook: DB-connection-timeout")

### 4.7 Ask Aegis
- Chat panel; assistant answers with **read-only tools**, showing each tool call
  ("get_metrics('api-gateway', 'p95', 15m) → 1.42 s") and cited evidence
- Disclaimer bar: "Aegis can only read — it cannot change anything without your approval"

## 5. The Final Demo Story (product-level)

```text
1. Command Center is green; autonomy mode: SAFE-AUTO
2. Chaoslab injects a database failure (visible to the audience: `chaoslab inject db-down`)
3. Anomaly fire within seconds → incident card appears (sev1) → MTTD timer starts
4. AI investigates: metrics, logs, traces, recent deploys → hypothesis card:
   "Postgres unavailable since 10:14:32 — API p95 rose, connection errors in logs" (all cited)
5. Remediation recommended: "Restart postgres (low risk, reversible)" → auto-executed (SAFE-AUTO)
   — or a higher-risk action requiring the lead's one-click approval, shown live
6. Recovery verification: health restored, error rate 0, SLO budget safe → incident closed
7. MTTD/MTTR stats update on the Command Center; AI postmortem generated
8. Audience can type "what happened at 10:14?" in Ask Aegis and get the cited answer
```

## 6. Non-Goals (visual/product)

- No mobile app; desktop browser only (demo runs full-screen).
- No public internet deployment required — the demo runs on the local cluster.
- No marketing-grade polish; professional dark console is enough.
- The console is not the monitored app — it is the *control plane for* the monitored app.
