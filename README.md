# Book Catalogue API (XJCO3011)

REST API for managing a **book catalogue** with full **CRUD** on a **SQLite** database, plus a small **analytics** endpoint. Built with **FastAPI** and **SQLAlchemy 2**.

**Repository:** [https://github.com/RuncongZhou/xjco3011-coursework-api](https://github.com/RuncongZhou/xjco3011-coursework-api)

## Features

- One main data model: `Book` (title, author, ISBN, year, genre, pages, rating, notes).
- CRUD over HTTP with JSON request/response bodies.
- Conventional status codes: `201` create, `200` OK, `204` delete, `404` not found, `409` duplicate ISBN, `422` validation.
- Interactive docs: Swagger UI at `/docs`, ReDoc at `/redoc`, OpenAPI schema at `/openapi.json`.
- Optional sample data via `scripts/seed_books.py`.
- Basic automated tests with `pytest`.

## Requirements

- Python **3.11+** (3.10 should work; use 3.11+ if possible).

## Quick start

```bash
cd xjco3011-coursework-api
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### Run the server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API base URL: `http://127.0.0.1:8000/api/v1`
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Optional: load sample books

```bash
python scripts/seed_books.py
```

### Optional: custom database path

Copy `.env.example` to `.env` and set `DATABASE_URL`, for example:

```env
DATABASE_URL=sqlite:///./data/books.db
```

### Tests

```bash
pytest
```

## API documentation (coursework submission)

The brief asks for API documentation **referenced from the README as a PDF**. You can satisfy this in either of these ways:

1. **Print Swagger to PDF:** open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in the browser → Print → Save as PDF → commit as e.g. `docs/API_DOCUMENTATION.pdf`.
2. **Use the Markdown companion:** edit if needed, then export `docs/API_DOCUMENTATION.md` to PDF (VS Code / Word / Pandoc), and commit as `docs/API_DOCUMENTATION.pdf`.

Generate machine-readable OpenAPI JSON (useful for reports):

```bash
python scripts/export_openapi.py
```

Output: `docs/openapi.json`.

## Endpoints (summary)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Service metadata |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/books` | Create a book |
| `GET` | `/api/v1/books` | List books (pagination, optional `genre`, `author`) |
| `GET` | `/api/v1/books/stats/summary` | Totals, average rating, counts by genre |
| `GET` | `/api/v1/books/{id}` | Get one book |
| `PATCH` | `/api/v1/books/{id}` | Update a book |
| `DELETE` | `/api/v1/books/{id}` | Delete a book |

Full request/response examples are in `docs/API_DOCUMENTATION.md` and in the interactive `/docs` UI.

## Project layout

```
app/
  main.py          # FastAPI app, CORS, lifespan (creates tables)
  config.py        # Settings (env / .env)
  database.py      # Engine, Session, Base
  models.py        # SQLAlchemy models
  schemas.py       # Pydantic request/response models
  crud.py          # Database operations
  routers/books.py # HTTP routes
data/              # SQLite file created at runtime (gitignored except .gitkeep)
docs/              # Human-readable API doc + exported OpenAPI
scripts/           # Seed + OpenAPI export
tests/             # Pytest
```

## Licence

Provided for academic submission; adapt as required by your module.
