import {
  MOCK_DEPLOYMENTS,
  MOCK_SERVICES,
  type Deployment,
  type ServiceInfo,
  type ServiceStatus,
} from "./mocks";

export type DataSource = "live" | "mock";

function asStatus(value: unknown): ServiceStatus {
  if (value === "healthy" || value === "degraded" || value === "unhealthy" || value === "unknown") {
    return value;
  }
  return "unknown";
}

export async function loadServices(): Promise<{ items: ServiceInfo[]; source: DataSource }> {
  const base = process.env.REGISTRY_URL;
  if (!base) {
    return { items: MOCK_SERVICES, source: "mock" };
  }
  try {
    const res = await fetch(`${base.replace(/\/$/, "")}/services`, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`registry ${res.status}`);
    }
    const rows: unknown = await res.json();
    if (!Array.isArray(rows) || rows.length === 0) {
      throw new Error("empty registry");
    }
    const items: ServiceInfo[] = rows.map((row) => {
      const rec = row as Record<string, unknown>;
      return {
        id: String(rec.id ?? ""),
        name: String(rec.name ?? rec.id ?? "service"),
        url: String(rec.url ?? ""),
        version: String(rec.version ?? "0.1.0"),
        status: asStatus(rec.status),
      };
    });
    return { items, source: "live" };
  } catch {
    return { items: MOCK_SERVICES, source: "mock" };
  }
}

export async function loadDeployments(): Promise<{ items: Deployment[]; source: DataSource }> {
  const base = process.env.DEPLOYMENTS_URL;
  if (!base) {
    return { items: MOCK_DEPLOYMENTS, source: "mock" };
  }
  try {
    const res = await fetch(`${base.replace(/\/$/, "")}/deployments?limit=20`, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`deployments ${res.status}`);
    }
    const rows: unknown = await res.json();
    if (!Array.isArray(rows)) {
      throw new Error("bad deployments payload");
    }
    const items: Deployment[] = rows.map((row) => {
      const rec = row as Record<string, unknown>;
      const status = rec.status;
      return {
        eventId: String(rec.event_id ?? ""),
        service: String(rec.service ?? ""),
        revision: String(rec.revision ?? ""),
        status: status === "in_progress" || status === "failed" ? status : "succeeded",
        storedAt: String(rec.stored_at ?? ""),
      };
    });
    return { items, source: "live" };
  } catch {
    return { items: MOCK_DEPLOYMENTS, source: "mock" };
  }
}
