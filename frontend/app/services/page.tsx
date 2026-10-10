import { loadServices } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function ServicesPage() {
  const { items: MOCK_SERVICES, source } = await loadServices();
  return (
    <>
      <div className="topbar">
        <div>
          <h1 style={{ margin: 0 }}>Services</h1>
          <p className="muted">
            Registry A2 · {source === "live" ? "live API" : "mock payload"}
          </p>
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
