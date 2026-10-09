# oxzoo-fastapi-react

Deployed with [ox](https://deploywithox.com): deploy a repo to your own server with one command, no Docker. [Docs](https://deploywithox.com/docs) · [Guide for this stack](https://deploywithox.com/docs/guides/fastapi)

An [ox](https://deploywithox.com) deploy example: a FastAPI backend with a React 18 SPA, deployed to your own Ubuntu server. uv installs and runs the backend, npm builds the frontend, systemd runs uvicorn, and Caddy serves the built `dist/` while sending the API paths to uvicorn.

## Stack

| Layer | Tool | Version |
|---|---|---|
| Backend | FastAPI | 0.141.1 |
| Server | uvicorn (Python 3.13, uv) | 0.53.0 |
| Database | SQLAlchemy 2, psycopg 3, alembic | |
| Frontend | React + React DOM | 18.3.1 |
| Bundler | Vite + @vitejs/plugin-react | 5.4.21 / 4.7.0 |
| Services | PostgreSQL 18 (pgcrypto), Redis 8 | provided by ox from `[services]` |

## ox.toml

```toml
# FastAPI (uv) + alembic migrations + pgcrypto, and a React SPA.

[app]
start  = "uv run uvicorn main:app --host 127.0.0.1 --port $PORT"
health = "/health"

[static]
dir = "dist"
spa = true
api = ["/api", "/health"]

[build]
commands = ["uv sync --frozen --no-dev", "npm run build"]
migrate  = "uv run alembic upgrade head"

[services]
postgres = { extensions = ["pgcrypto"] }
redis    = {}

[tools]
node = "24"
```

The repo has two lockfiles, so ox's detected install is `npm ci` and `[build] commands` adds `uv sync` before the SPA build. `[build] migrate` runs alembic before traffic switches, and ox snapshots the database first.

## Services

- **postgres:** `DATABASE_URL`. Every `/api/greeting` hit inserts one row into `greeting_log`; `GET /api/stats` returns its row count. alembic creates the schema, including the `pgcrypto` extension used for `gen_random_uuid()` ids.
- **redis:** `REDIS_URL`. `GET /api/visits` increments `oxzoo:visits` and sets a one-hour TTL on the first hit.

`db.py` and `main.py` fall back to local addresses when the variables are unset, for local development.

## Environment flow

- **Backend, run time:** `GET /api/greeting` reads `GREETING_TAG` on every request.
- **Frontend, build time:** `src/App.jsx` reads `import.meta.env.GREETING_TAG`, which Vite inlines because `vite.config.js` sets `envPrefix: ["GREETING_", "VITE_"]`. ox sets your variables before the build, and changing one with `ox vars set` redeploys, which rebuilds the SPA.

## Deploy with ox

```sh
curl -fsSL https://deploywithox.com/install.sh | sh
ox login
ox new https://github.com/saurav-codes/oxzoo-fastapi-react
printf 'GREETING_TAG=demo\n' | ox review oxzoo-fastapi-react --from-file - --wait
```

The plan, offline:

```console
$ ox check .
ox check . (manifest: ox.toml)

  app.start                  uv run uvicorn main:app --host 127.0.0.1 --port $PORT declared
  app.health                 /health                                              declared
  static.dir                 dist                                                 declared
  static.spa                 true                                                 declared
  static.api                 /api, /health                                        declared
  build.install              npm ci                                               detected:package-lock.json
  build.commands[0]          uv sync --frozen --no-dev                            declared
  build.commands[1]          npm run build                                        declared
  build.migrate              uv run alembic upgrade head                          declared
  tools.node                 24                                                   declared
  tools.python               3.13                                                 detected:.python-version
  tools.uv                   0.11                                                 default
  services.postgres          postgres 18 (shared)                                 default
  services.redis             redis 8 (only for this project)                      default

  Provided by ox: PORT, HOST, OX_ENV, OX_PROJECT, OX_RELEASE, OX_DATA_DIR, PUBLIC_URL, PUBLIC_HOST, DATABASE_URL, REDIS_URL
  Set on the dashboard before the first deploy: GREETING_TAG

Ready to deploy.
```

## Expected output

```
frontend: hello world oxzoo-fastapi-react_<GREETING_TAG>
backend: hello world oxzoo-fastapi-react_<GREETING_TAG>
```

The frontend line is baked at build time; the backend line comes from the running process.

## Local development

```sh
uv sync && npm install
uv run alembic upgrade head            # needs a local PostgreSQL, or export DATABASE_URL
GREETING_TAG=dev npm run build
GREETING_TAG=dev uv run uvicorn main:app --port 8000
```
