import { MOCK_DEPLOYMENTS } from "@/lib/mocks";

export default function DeploymentsPage() {
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Deployments</h1>
          <p className="muted">DI-1 history shape · mock until live API is selected in the UI</p>
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
