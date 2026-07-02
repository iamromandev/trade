# Trade Backend

Production-ready FastAPI backend with PostgreSQL, Tortoise ORM, JWT auth, and full middleware stack.

## Quick Start

```bash
cp .env.example .env
make up
curl http://localhost:8000/api/v1/health/check
```

## Local Development

```bash
cp .env.example .env
make install
make migrate
make run
```

## Project Structure

```
src/
├── auth/         # JWT, OAuth2, RBAC
├── config/       # Settings, logging
├── core/         # Base classes, types, errors
├── data/db/      # Models, repos, migrations
├── infra/        # Cache, event bus, storage
├── module/       # Feature modules (health, user)
├── shared/       # Middleware, deps, util
└── task/         # Background workers
```
