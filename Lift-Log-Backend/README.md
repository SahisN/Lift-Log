# Lift-Log Backend

REST API for Lift-Log, a workout tracker. It stores an exercise catalog, each user's current numbers for an exercise (an *exercise profile*), and a history log for each profile.

## Tech stack

| Area            | Tool                                                        |
| --------------- | ----------------------------------------------------------- |
| Language        | Python 3.14                                                 |
| Package manager | [uv](https://docs.astral.sh/uv/)                            |
| Web framework   | FastAPI                                                     |
| ORM             | SQLAlchemy 2 (async) with the `asyncpg` driver              |
| Migrations      | Alembic (with the sync `psycopg` 3 driver)                  |
| Validation      | Pydantic v2, pydantic-settings                              |
| Database        | PostgreSQL 17                                               |
| Local DB        | testcontainers (dev dependency) or Docker Compose           |

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.14 for you if you don't have it.
- [Docker](https://docs.docker.com/get-docker/), running. The quick start uses it to start Postgres automatically.

## Quick start (zero config)

Run everything from this directory (`Lift-Log-Backend/`):

```bash
uv sync
uv run fastapi dev app/server.py
```

With no `.env` file, the app starts a temporary `postgres:17-alpine` container, applies all migrations to it, and stops it when the server shuts down. **All data is lost on restart.**

Once it's running:

- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Running against your own Postgres

To keep data between restarts, point the app at a real database. Create a `.env` file in this directory:

```dotenv
# Used by the app (async driver)
ASYNC_DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/liftlog

# Used by Alembic (sync driver)
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/liftlog
```

When `ASYNC_DATABASE_URL` is set, the app does **not** migrate on startup, so apply migrations yourself first:

```bash
uv run alembic upgrade head
uv run fastapi dev app/server.py
```

## Database migrations

Migrations live in `app/alembic/versions/`.

```bash
uv run alembic upgrade head                        # apply migrations
uv run alembic revision --autogenerate -m "msg"    # generate a new migration
```

Autogenerate compares your models to a live database. If `DATABASE_URL` is unset, Alembic starts an **empty** container, and autogenerate will then produce a migration for the entire schema. To get a correct diff, use the Docker Compose database in `../Lift-Log-DB/Alembic-migration-DB/`:

```bash
docker compose -f ../Lift-Log-DB/Alembic-migration-DB/docker-compose.yml up -d

export DATABASE_URL=postgresql+psycopg://test:test@localhost:5432/liftlog
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "describe your change"

docker compose -f ../Lift-Log-DB/Alembic-migration-DB/docker-compose.yml down
```

This Compose database keeps its data in memory (tmpfs), so it starts empty every time.

When you add a new model, import it in `app/alembic/env.py` too, or autogenerate won't see it.

## Configuration

- `config.yaml`: settings that aren't secret (app name, database and pagination options).
- `.env`: database URLs (see above). It's git-ignored.

Both files are read from the current directory, so run commands from `Lift-Log-Backend/`.

## Project structure

```
app/
├── server.py          # FastAPI app and startup/shutdown (lifespan)
├── db.py              # engine, sessions, testcontainer startup
├── settings.py        # loads config.yaml and .env
├── api/routes/        # routers; versioned endpoints in v1/
├── services/          # business logic
├── repos/             # database queries
├── models/            # SQLAlchemy models and typed IDs
├── schemas/           # Pydantic request/response models
├── errors/            # domain errors mapped to HTTP status codes
└── alembic/           # migration environment and versions
```

A request goes **route → service → repo → database**. The routes, services and repos are wired together with FastAPI `Depends`, in `repos/deps/wiring.py` and `services/deps/wiring.py`. Each request gets one database session, which is committed when the request succeeds and rolled back when it raises an error.

## Linting

Ruff is configured in `pyproject.toml` but isn't a project dependency, so run it through `uvx`:

```bash
uvx ruff check app
```
