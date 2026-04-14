# Book Catalogue API — Documentation

**Base URL (local default):** `http://127.0.0.1:8000`  
**API prefix:** `/api/v1`  
**Media type:** `application/json`  
**Authentication:** none (coursework baseline; document as “not implemented” or extend in your report if you add API keys).

---

## Conventions

- **Success:** JSON body with `Content-Type: application/json`.
- **Validation errors:** HTTP `422` with FastAPI’s default error shape (`detail` array).
- **Not found:** HTTP `404`, body `{"detail": "Book not found"}`.
- **Conflict (duplicate ISBN):** HTTP `409`, body `{"detail": "ISBN already exists for another book."}`.

---

## 1. Service metadata

### `GET /`

**Response `200`**

```json
{
  "service": "Book Catalogue API",
  "docs": "/docs",
  "openapi": "/openapi.json",
  "api_base": "/api/v1"
}
```

---

## 2. Health

### `GET /health`

**Response `200`**

```json
{ "status": "ok" }
```

---

## 3. Create book

### `POST /api/v1/books`

**Request body**

| Field | Type | Required | Notes |
|--------|------|----------|--------|
| `title` | string | yes | 1–500 chars |
| `author` | string | yes | 1–300 chars |
| `isbn` | string | no | unique if set |
| `publication_year` | integer | no | 1000–2100 |
| `genre` | string | no | e.g. Fiction, Technology |
| `pages` | integer | no | ≥ 0 |
| `rating` | number | no | 0–10 |
| `notes` | string | no | free text |

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
| `limit` | int | 20 | Page size (1–100) |
| `genre` | string | — | Exact match on genre |
| `author` | string | — | Case-insensitive substring match |

**Response `200`:** JSON array of book objects (same shape as in §3).

---

## 5. Statistics

### `GET /api/v1/books/stats/summary`

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

---

## 6. Get one book

### `GET /api/v1/books/{book_id}`

**Response `200`:** single book object.  
**Response `404`:** `{"detail":"Book not found"}`.

---

## 7. Update book

### `PATCH /api/v1/books/{book_id}`

Send only fields to change (all optional).

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

**Response `204`:** no body.  
**Response `404`:** not found.

---

## Interactive documentation

With the server running, open **Swagger UI:** `/docs` — try requests directly from the browser.

---

## Export for submission

- **PDF:** print `/docs` to PDF, or export this file from your editor, and commit as `docs/API_DOCUMENTATION.pdf` alongside this repository.
- **OpenAPI JSON:** run `python scripts/export_openapi.py` → `docs/openapi.json`.
