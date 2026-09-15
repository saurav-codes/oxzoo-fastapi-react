# oxzoo-fastapi-react

The official ox deploy example for a FastAPI backend with a React 18 SPA frontend on one Ubuntu VPS (systemd + nginx). uv resolves and runs the Python backend, npm builds the frontend, and ox wires up nginx to serve the built `dist/` while proxying the API. Clone, set one environment variable, press Deploy.

## Stack

| Layer | Tool | Pinned version |
|---|---|---|
| Backend | FastAPI | 0.141.1 |
| Backend server | uvicorn (via uv, Python 3.13) | 0.53.0 |
| Frontend | React + React DOM (npm) | 18.3.1 |
| Bundler | Vite + @vitejs/plugin-react | 5.4.21 / 4.7.0 |
| Serving | nginx (SPA) + systemd (uvicorn on 127.0.0.1:9110) | managed by ox |

## Environment flow

One variable, two different moments:

- **Backend, runtime**: `GET /api/greeting` reads `GREETING_TAG` from `os.environ` on every request. ox injects the value from the Environment editor into the service's environment file, so changing the tag needs only a process restart, never a rebuild.
- **Frontend, build time**: `src/App.jsx` reads `import.meta.env.GREETING_TAG`, which Vite inlines at build time because `vite.config.js` sets `envPrefix: ["GREETING_", "VITE_"]`. The deploy's `npm run build` hook bakes the value into `dist/`, so changing it means redeploying.
- **Serving**: nginx serves `dist/` from the current release with an `index.html` fallback (SPA mode) and proxies `/api` and `/health` to uvicorn on 127.0.0.1:9110.

Copy `.env.example` to `.env` for local work only. Never commit `.env`; on the VPS, values live in the ox Environment editor, not in git.

## Deploy with ox

1. Paste the clone URL (`https://github.com/saurav-codes/oxzoo-fastapi-react.git`) into the ox dashboard.
2. Set `GREETING_TAG` (placeholder: `GREETING_TAG=dev-01`) in the Environment editor BEFORE the first deploy: the install and build hooks bake it into the frontend, and the runtime reads it for the backend.
3. Press Deploy. ox validates `ox.toml`, runs `uv sync --frozen` and `npm install`, builds `dist/`, starts the uvicorn systemd unit, polls `/health`, then switches nginx.

## Expected output

With `GREETING_TAG=<tag>` set before deploying:

```
frontend: hello world oxzoo-fastapi-react_<tag>
backend: hello world oxzoo-fastapi-react_<tag>
```

The frontend line is baked at build time; the backend line comes from the live environment.
