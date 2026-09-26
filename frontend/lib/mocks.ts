export type ServiceStatus = "healthy" | "degraded" | "unhealthy" | "unknown";

export type ServiceInfo = {
  id: string;
  name: string;
  url: string;
  version: string;
  status: ServiceStatus;
};

export type Incident = {
  id: string;
  title: string;
  severity: "sev1" | "sev2" | "sev3" | "sev4";
  status: "open" | "investigating" | "remediating" | "verifying" | "closed";
  service: string;
  openedAt: string;
};

export type Deployment = {
  eventId: string;
  service: string;
  revision: string;
  status: "in_progress" | "succeeded" | "failed";
  storedAt: string;
};

export const MOCK_SERVICES: ServiceInfo[] = [
  { id: "catalog-service", name: "AegisShop Catalog", url: "http://localhost:9001", version: "0.1.0", status: "healthy" },
  { id: "cart-service", name: "AegisShop Cart", url: "http://localhost:9002", version: "0.1.0", status: "healthy" },
  { id: "order-service", name: "AegisShop Order", url: "http://localhost:9003", version: "0.1.0", status: "healthy" },
  { id: "payment-service", name: "AegisShop Payment", url: "http://localhost:9004", version: "0.1.0", status: "healthy" },
  { id: "registry-service", name: "Registry", url: "http://localhost:8101", version: "0.1.0", status: "healthy" },
  { id: "deployments-service", name: "Deployments", url: "http://localhost:8701", version: "0.1.0", status: "healthy" },
];

export const MOCK_INCIDENTS: Incident[] = [
  {
    id: "inc-0001",
    title: "Seed incident (mock) — waiting for A3/A4 in P3",
    severity: "sev4",
    status: "closed",
    service: "catalog-service",
    openedAt: "2026-09-20T09:00:00Z",
  },
];

export const MOCK_DEPLOYMENTS: Deployment[] = [
  {
    eventId: "evt_01J8B2ABC",
    service: "catalog-service",
    revision: "v0.1.0",
    status: "succeeded",
    storedAt: "2026-09-08T10:00:00Z",
  },
];

export const MOCK_STATS = {
  mttdSeconds: 12,
  mttrSeconds: 0,
  openIncidents: 0,
  autonomyMode: "OBSERVE" as const,
};
