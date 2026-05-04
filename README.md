# bot-over-signals

Backend base for a football Over markets signal bot.

This first sprint intentionally implements only the project setup:

- FastAPI application
- Health check routes
- PostgreSQL connection setup with SQLAlchemy 2.x
- Alembic migrations setup
- Redis service in Docker Compose
- pytest test suite

No betting automation, Telegram integration, scraping, authentication, or domain models are implemented yet.

## Requirements

- Python 3.12+
- Docker and Docker Compose

## Environment

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

The example uses local development credentials only.

## Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at:

- `http://localhost:8000/health`
- `http://localhost:8000/api/v1/health`

Expected response:

```json
{
  "status": "ok",
  "service": "bot-over-signals"
}
```

## Run Tests Locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

## Alembic

Alembic is configured and ready for future migrations.

Create a migration after adding SQLAlchemy models:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Apply migrations:

```bash
alembic upgrade head
```

## Current Scope

This repository is only the technical foundation for future features:

- registering externally validated methods from Zeus/Full Trader
- collecting live matches
- evaluating matches against methods
- sending Telegram signals
- auditing signals and results
