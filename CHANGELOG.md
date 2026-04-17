# Changelog

All notable changes to this project are documented here (useful for assessors reviewing Git history).

## 1.2.0 — 2026-04-14

- Add **GitHub Actions CI** workflow: runs `pytest` on every push to `main`.
- Add **Dockerfile** and **docker-compose** for optional containerised deployment.
- Expand **automated tests** (root endpoint, validation errors, pagination, empty stats).
- Enrich **OpenAPI metadata** (contact URL, licence summary) in `app.main`.
- Document **data sources / licensing** for seed metadata (`docs/DATA_SOURCES.md`).

## 1.1.0 — earlier

- Pagination (`items`, `total`), search `q`, sort/order, optional `API_KEY` for writes, DB health check.

## 1.0.0 — initial

- Book CRUD, SQLite, Swagger/OpenAPI, seed script, pytest baseline.
