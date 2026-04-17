# Book Catalogue API - API documentation

**Base URL (local default):** `http://127.0.0.1:8000`  
**API prefix:** `/api/v1`  
**Media type:** `application/json`  
**Authentication:** **Optional.** If the server is configured with environment variable `API_KEY`, then `POST`, `PATCH`, and `DELETE` must include header `X-API-Key: <same value>`. If `API_KEY` is not set (default for local development), writes do not require a key. `GET` endpoints are always public.

**Version:** `1.2.0` (see `GET /` and `app/config.py`).

---

## Conventions

- **Success:** JSON body with `Content-Type: application/json`.
- **Validation errors:** HTTP `422` with FastAPI default error shape (`detail` array).
- **Not found:** HTTP `404`, body `{"detail": "Book not found"}`.
- **Conflict (duplicate ISBN):** HTTP `409`, body `{"detail": "ISBN already exists for another book."}`.
- **Unauthorized (API key):** HTTP `401`, body `{"detail": "Missing or invalid X-API-Key header."}` when `API_KEY` is set but `X-API-Key` is missing or wrong (writes only).
- **Service unavailable:** HTTP `503` from `GET /health` if the database cannot be reached, body `{"detail": "Database unavailable"}`.

---

## 1. Service metadata

### `GET /`

**Response `200`**

```json
{
  "service": "Book Catalogue API",
  "version": "1.2.0",
  "repository": "https://github.com/RuncongZhou/xjco3011-coursework-api",
  "docs": "/docs",
  "openapi": "/openapi.json",
  "api_base": "/api/v1",
  "write_protection": false
}
```

(`write_protection` is `true` when `API_KEY` is configured.)

---

## 2. Health

### `GET /health`

**Response `200`**

```json
{ "status": "ok", "database": "connected" }
```

**Response `503`** (database unreachable)

```json
{ "detail": "Database unavailable" }
```

---

## 3. Create book

### `POST /api/v1/books`

**Headers (when `API_KEY` is set):** `X-API-Key: <your API key>`

**Request body**

| Field | Type | Required | Notes |
|--------|------|----------|--------|
| `title` | string | yes | 1-500 chars |
| `author` | string | yes | 1-300 chars |
| `isbn` | string | no | max 20 chars; unique if set |
| `publication_year` | integer | no | 1000-2100 |
| `genre` | string | no | max 120 chars |
| `pages` | integer | no | >= 0 |
| `rating` | number | no | 0-10 |
| `notes` | string | no | optional free text |

**Example request**

```http
POST /api/v1/books HTTP/1.1
Content-Type: application/json

{
  "title": "The Pragmatic Programmer",
  "author": "David Thomas",
  "isbn": "978-0135957059",
  "publication_year": 2019,
  "genre": "Technology",
  "pages": 352,
  "rating": 9.2
}
```

**Response `201`**

```json
{
  "title": "The Pragmatic Programmer",
  "author": "David Thomas",
  "isbn": "978-0135957059",
  "publication_year": 2019,
  "genre": "Technology",
  "pages": 352,
  "rating": 9.2,
  "notes": null,
  "id": 1,
  "created_at": "2026-04-14T12:00:00Z",
  "updated_at": "2026-04-14T12:00:00Z"
}
```

---

## 4. List books

### `GET /api/v1/books`

**Query parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `skip` | int | 0 | Offset |
| `limit` | int | 20 | Page size (1-100) |
| `genre` | string | (none) | Exact match on genre |
| `author` | string | (none) | Case-insensitive substring match on author |
| `q` | string | (none) | Search substring in title, author, or ISBN (max 200 chars) |
| `sort` | string | `created_at` | One of: `created_at`, `title`, `rating`, `publication_year` |
| `order` | string | `desc` | `asc` or `desc` |

**Response `200`:** paginated wrapper:

```json
{
  "items": [ { "id": 1, "title": "...", "...": "same shape as create response" } ],
  "total": 42,
  "skip": 0,
  "limit": 20
}
```

Each element of `items` matches the book object returned by create (section 3) and get-one (section 6).

---

## 5. Statistics

### `GET /api/v1/books/stats/summary`

Registered as a static path before `/{book_id}`, so `stats` is not interpreted as a numeric id.

**Response `200`**

```json
{
  "total_books": 3,
  "average_rating": 9.1,
  "genres": {
    "Technology": 3
  }
}
```

(`average_rating` may be `null` if no ratings are stored.)

---

## 6. Get one book

### `GET /api/v1/books/{book_id}`

**Response `200`:** single book object.  
**Response `404`:** `{"detail":"Book not found"}`.

---

## 7. Update book

### `PATCH /api/v1/books/{book_id}`

**Headers (when `API_KEY` is set):** `X-API-Key: <your API key>`

Send only fields to change (all optional). Field constraints match create (section 3) where applicable.

**Example**

```json
{ "rating": 9.5, "notes": "Recommended" }
```

**Response `200`:** updated book.  
**Response `404`:** not found.  
**Response `409`:** ISBN conflict.

---

## 8. Delete book

### `DELETE /api/v1/books/{book_id}`

**Headers (when `API_KEY` is set):** `X-API-Key: <your API key>`

**Response `204`:** no body.  
**Response `404`:** not found.

---

## Interactive documentation

With the server running, open **Swagger UI** at `/docs` to try requests from the browser. **ReDoc** is at `/redoc`. Machine-readable schema: `/openapi.json` (see also `docs/openapi.json` from `scripts/export_openapi.py`).

---

## Export for submission

- **PDF:** print `/docs` to PDF, export this Markdown from your editor, or run `pandoc docs/API_DOCUMENTATION.md -o docs/API_DOCUMENTATION.pdf` if Pandoc is installed. Commit `docs/API_DOCUMENTATION.pdf` if your brief requires a PDF in the repo.
- **OpenAPI JSON:** `python scripts/export_openapi.py` writes `docs/openapi.json`.
