# AegisDeploy Console (P2 scaffold)

Dark observability console for AegisDeploy. P2 ships the shell, design tokens,
and Command Center / services / incidents / deployments pages on **mock data**.
Live API wiring starts when A2/DI-1 are consumed in a later increment.

```bash
cd frontend
npm install
npm run dev    # http://localhost:3030
```

Grafana keeps host port **3000**; the console uses **3030** so both can run.
Dev CORS on backend services allows `http://localhost:3000` and `http://localhost:3030`.
