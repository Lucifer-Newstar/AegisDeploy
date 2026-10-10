import { loadDeployments } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function DeploymentsPage() {
  const { items: MOCK_DEPLOYMENTS, source } = await loadDeployments();
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Deployments</h1>
          <p className="muted">
            DI-1 history · {source === "live" ? "live API" : "mock payload"}
          </p>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Event</th>
              <th>Service</th>
              <th>Revision</th>
              <th>Status</th>
              <th>Stored</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_DEPLOYMENTS.map((row) => (
              <tr key={row.eventId}>
                <td>{row.eventId}</td>
                <td>{row.service}</td>
                <td>{row.revision}</td>
                <td>
                  <span className="pill healthy">{row.status}</span>
                </td>
                <td className="muted">{row.storedAt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
