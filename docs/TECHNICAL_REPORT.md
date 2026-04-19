Technical Report: Book Catalogue Web API
Module: XJCO3011 Web Services and Web Data
Assessment: Coursework 1 — Individual Web Services API Development Project
Date: April 2026
Repository: https://github.com/RuncongZhou/xjco3011-coursework-api

1. Introduction and aims
This project implements a data-driven REST API [5] for managing a book catalogue backed by a relational (SQL) database. The service exposes HTTP endpoints for Create, Read, Update, and Delete (CRUD) operations on a Book entity, together with list filtering, search, sorting, pagination metadata, and a small analytics endpoint that returns aggregate statistics (for example counts by genre and average rating).
The work is aligned with the module aim of applying software-engineering practice to API design: clear resource naming, consistent JSON payloads, conventional HTTP status codes, and machine-readable documentation via OpenAPI [6] and the FastAPI-generated documentation [1]. The implementation is intentionally self-contained (no third-party book API calls at runtime); optional seed data can be loaded from a script for demonstrations.

2. High-level architecture
The system follows a layered structure. First, the HTTP layer (FastAPI routers [1]) validates input with Pydantic models [2], maps URLs to handlers, applies optional write authentication (X-API-Key when configured), and translates errors into HTTP responses (for example 401 for invalid or missing write credentials, 404 for missing entities, 409 for conflicts such as duplicate ISBN, and 422 for validation failures). Second, the application logic module encapsulates database operations (queries, pagination counts, statistics). Third, persistence uses the SQLAlchemy ORM [3] with SQLite [4], mapping the Book model to tables and managing sessions.

Figure 1. Swagger UI (OpenAPI) overview of the Book Catalogue API, showing books endpoints.

3. Technology stack and rationale
3.1 Programming language: Python
Python was chosen for rapid, readable development, strong ecosystem support for web services and data access, and compatibility with teaching materials that reference Django or FastAPI [1]. It integrates cleanly with pytest [7] for automated regression testing.
3.2 Web framework: FastAPI
FastAPI provides automatic OpenAPI documentation, Pydantic v2 integration for validation [2], and async-capable foundations (even where this coursework uses synchronous SQLAlchemy sessions for simplicity) [1]. These features reduce boilerplate and produce an inspectable contract at the /docs and /openapi.json routes, which matches the coursework requirement to supply API documentation alongside the implementation [6].
3.3 Database: SQLite via SQLAlchemy 2.0
The brief permits any SQL database; SQLite was selected for zero separate server process, simple coursework portability, and straightforward deployment in a single file under the data directory [4]. SQLAlchemy 2.0 offers a typed, maintainable ORM layer [3] and migrations-free bootstrapping for this scope (table creation on startup), which is appropriate for an individual prototype while remaining easy to justify in an oral exam.
If the project were scaled, a natural upgrade path would be PostgreSQL (still SQL) with Alembic migrations (see [3]), preserving the stack narrative while addressing concurrency and multi-user writes.
3.4 Testing and quality assurance
pytest exercises representative behaviours: successful CRUD flows, 404 for missing IDs, 422 validation failures, duplicate ISBN conflicts (409), pagination behaviour, optional API key enforcement (401), and basic analytics on an empty dataset [7]. GitHub Actions runs the suite on each push to the main branch, providing an auditable continuous integration signal compatible with the rubric’s emphasis on testing discipline.

Figure 2. JSON response from GET /health confirming API and database availability.

3.5 Repository, version control, and documentation packaging
The source code is maintained in the public GitHub repository identified above to satisfy the coursework requirement for visible version control. Development follows a simple single-branch model on main: incremental commits with descriptive messages after each coherent change (features, fixes, documentation), rather than a single bulk upload. This produces an auditable history for examiners and supports the oral examination discussion of how the solution evolved.
The repository root includes a README that explains environment setup, how to run the API locally, optional Docker usage, how to run tests, and where API documentation artefacts live. A Python-oriented .gitignore reduces risk of committing virtual environments, local SQLite databases, or environment files containing secrets. CHANGELOG.md summarises notable releases for readability; the API description for assessors is supplied both interactively (Swagger at /docs) and as companion Markdown under docs/, with a PDF export referenced from the README as required by the brief.

Figure 3. GitHub Actions workflow run: CI job “test” completed successfully after push to main.

3.6 Configuration, CORS, and reproducibility
Runtime settings are loaded with pydantic-settings from environment variables and an optional .env file (see .env.example in the repository). DATABASE_URL selects the SQLite path; API_KEY, when set, enables write protection as described in §4.3. This keeps secrets out of source control while remaining straightforward for local development and CI, where variables are injected by the shell or the workflow file rather than committed files.
The application enables permissive CORS middleware so browser-based clients (including Swagger UI and small demonstration front-ends) can call the API during teaching and oral sessions without preflight failures on a typical laptop setup. This is appropriate for a coursework service exposed on localhost; a production deployment would restrict allow_origins to known front-end hosts.
For assessors who prefer an offline contract, python scripts/export_openapi.py writes docs/openapi.json from the same FastAPI application object used at runtime, so the saved schema matches /openapi.json when the server is running.

4. API design decisions
4.1 RESTful resources
Books are exposed under the /api/v1/books path. Collection reads return a paginated wrapper (items, total, skip, limit) rather than a bare array, to make client implementation and demonstration of paging easier. This aligns with resource-oriented HTTP design as discussed in the REST architectural style [5]. The list payload always returns total together with items so a client can show “page x of y” without loading every row into memory.
Query features include q (substring match across title, author, ISBN), genre, author, and sort / order for transparent analytics-style use cases without introducing a separate query language. Together these filters support search and browsing scenarios beyond a minimal CRUD demo while keeping a single REST resource model. An additional GET route returns summary statistics (for example totals and averages by genre), which satisfies the analytics-style requirement without introducing GraphQL or a second API style.
4.2 Status and error model
The API uses conventional codes: 201 Created on insert, 204 No Content on delete, 404 when an entity is missing, 409 on unique ISBN conflicts, 422 where input fails validation, 401 Unauthorized when mutating requests are protected and the X-API-Key header is missing or incorrect, and 503 if health checks detect database failure. Error bodies follow FastAPI’s JSON detail pattern for consistency [1].
4.3 Authentication
Write operations (POST, PATCH, DELETE) support an optional API key supplied through the X-API-Key header when API_KEY is set in the environment. This is documented as an authentication mechanism where applicable in the spirit of the brief: it demonstrates defence-in-depth thinking for public coursework demos while keeping local development friction low (no key required if unset).

5. Data sources, licensing, and seeding
Runtime records are stored locally in SQLite [4]. The optional seed script inserts example rows with metadata referencing well-known published works; bibliographic-style citations and licensing considerations are discussed in the project file docs/DATA_SOURCES.md. The coursework encourages public datasets; here the emphasis is on transparent provenance and academic honesty rather than importing large external corpora, which is compatible with a narrow but well-explained scope.

6. Challenges, testing strategy, and lessons learned
Challenges encountered included reconciling pagination totals with filter predicates, ensuring route ordering so /stats/summary is not captured as an id path parameter, and managing duplicate ISBN constraints cleanly at the HTTP layer (409 instead of opaque ORM traces) [3].
Testing focused on behaviour observable at the HTTP boundary using FastAPI’s TestClient [1], with an isolated SQLite file for tests to avoid polluting development databases.
Lessons learned: auto-generated OpenAPI is valuable [6] but does not replace a short human-readable companion (docs/API_DOCUMENTATION.md) and a PDF export for submission, because assessors may review artefacts outside the running server. Continuous integration adds confidence but requires keeping dependencies installable in a clean environment.

7. Limitations and future improvements
Current limitations include SQLite concurrency for heavily parallel writes, schema evolution handled implicitly rather than via formal migrations, and no OAuth2 or JWT user accounts (only an optional static API key). Future work could add Alembic migrations, migrate to PostgreSQL [3], introduce role-based access, enrich analytics (recommendations, export formats), or integrate a public dataset import pipeline with scheduled refresh; each change should be justified against operational needs and licensing.

8. Generative AI (GenAI) declaration
I used the Cursor editor to assist with coding and with drafting parts of the project text. In practice that meant asking for small completions and refactors in the Python files, getting suggestions when tests failed or imports were wrong, and tightening wording in the README and API notes before I edited them myself.
This assignment is “green” for generative AI, so I also used Cursor to explore alternatives when I was unsure—for example how to structure pagination responses or whether to add a simple API key for writes. I decided what to adopt, ran the application and pytest on my machine, and rewrote or rejected suggestions that did not fit the brief. That division of labour left me more time to verify CRUD behaviour, status codes, and documentation than if I had written every line from scratch without assistance.

9. References
[1] Ramirez, S. (n.d.) FastAPI Documentation. Available at: https://fastapi.tiangolo.com/ (Accessed: 14 April 2026).
[2] Pydantic Project (n.d.) Pydantic Documentation. Available at: https://docs.pydantic.dev/latest/ (Accessed: 14 April 2026).
[3] Bayer, M. (n.d.) SQLAlchemy Documentation. Available at: https://docs.sqlalchemy.org/en/20/ (Accessed: 14 April 2026).
[4] SQLite Development Team (n.d.) SQLite Documentation. Available at: https://www.sqlite.org/docs.html (Accessed: 14 April 2026).
[5] Fielding, R.T. (2000) Architectural Styles and the Design of Network-based Software Architectures. Doctoral dissertation, University of California, Irvine. Available at: https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm (Accessed: 14 April 2026).
[6] OpenAPI Initiative (n.d.) OpenAPI Specification. Available at: https://spec.openapis.org/oas/latest.html (Accessed: 14 April 2026).
[7] pytest contributors (n.d.) pytest documentation. Available at: https://docs.pytest.org/en/stable/ (Accessed: 14 April 2026).
