import { loadServices } from "@/lib/data";
import { MOCK_INCIDENTS, MOCK_STATS } from "@/lib/mocks";

export const dynamic = "force-dynamic";

export default async function CommandCenterPage() {
  const { items: services, source } = await loadServices();
  const healthy = services.filter((s) => s.status === "healthy").length;
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Command Center</h1>
          <p className="muted">
            {source === "live" ? "Live registry" : "Mock data (registry unreachable)"}
            <span className="badge">P2 scaffold</span>
          </p>
        </div>
        <div className="mode">autonomy · {MOCK_STATS.autonomyMode}</div>
      </div>
      <div className="grid">
        <div className="card">
          <h3>Services healthy</h3>
          <div className="val">
            {healthy}/{services.length}
          </div>
        </div>
        <div className="card">
          <h3>Open incidents</h3>
          <div className="val">{MOCK_STATS.openIncidents}</div>
        </div>
        <div className="card">
          <h3>MTTD (demo)</h3>
          <div className="val">{MOCK_STATS.mttdSeconds}s</div>
        </div>
        <div className="card">
          <h3>MTTR (demo)</h3>
          <div className="val">—</div>
        </div>
      </div>
      <div className="card">
        <h3>Service health</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Service</th>
              <th>Status</th>
              <th>Version</th>
            </tr>
          </thead>
          <tbody>
            {services.map((svc) => (
              <tr key={svc.id}>
                <td>{svc.name}</td>
                <td>
                  <span className={`pill ${svc.status}`}>{svc.status}</span>
                </td>
                <td className="muted">{svc.version}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="card" style={{ marginTop: 16 }}>
        <h3>Incident feed</h3>
        {MOCK_INCIDENTS.length === 0 ? (
          <p className="muted">No incidents.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Title</th>
                <th>Sev</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {MOCK_INCIDENTS.map((inc) => (
                <tr key={inc.id}>
                  <td>{inc.id}</td>
                  <td>{inc.title}</td>
                  <td>
                    <span className={`pill ${inc.severity}`}>{inc.severity}</span>
                  </td>
                  <td>{inc.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
