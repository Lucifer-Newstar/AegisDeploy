import { MOCK_SERVICES } from "@/lib/mocks";

export default function ServicesPage() {
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Services</h1>
          <p className="muted">Registry shape from A2 contract · mock payload</p>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th>URL</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_SERVICES.map((svc) => (
              <tr key={svc.id}>
                <td>{svc.id}</td>
                <td>{svc.name}</td>
                <td className="muted">{svc.url}</td>
                <td>
                  <span className={`pill ${svc.status}`}>{svc.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
