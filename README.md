# SD Simulator Backend

FastAPI backend scaffold for SD Simulator.

## Setup

1. Create a virtual environment with Python 3.12+.
2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Copy `.env.example` to `.env` and update credentials:

```bash
cp .env.example .env
```

4. Run the API:

```bash
uvicorn app.main:app --reload
```

The API exposes health checks at:

- `GET /health`
- `GET /api/v1/health`

## Database

The expected MySQL database is `sd_simulator` on `localhost:3306`.

Use an async SQLAlchemy URL:

```env
DATABASE_URL=mysql+asyncmy://root:password@localhost:3306/sd_simulator
```

## Migrations

Create migrations with Alembic:

```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```
