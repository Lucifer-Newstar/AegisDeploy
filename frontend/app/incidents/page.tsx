import { MOCK_INCIDENTS } from "@/lib/mocks";

export default function IncidentsPage() {
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Incidents</h1>
          <p className="muted">A4 incident manager lands in P3 — this list is mocked.</p>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Title</th>
              <th>Service</th>
              <th>Sev</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_INCIDENTS.map((inc) => (
              <tr key={inc.id}>
                <td>{inc.id}</td>
                <td>{inc.title}</td>
                <td>{inc.service}</td>
                <td>
                  <span className={`pill ${inc.severity}`}>{inc.severity}</span>
                </td>
                <td>{inc.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
