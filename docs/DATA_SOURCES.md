# Data sources and licensing

## Runtime data

The API persists records in a **SQLite** database file (`data/books.db` by default). That file is **generated locally** when you run the application and is **not** committed to Git (see `.gitignore`).

## Seed script (`scripts/seed_books.py`)

The optional seed loader inserts a small set of **example book metadata** (title, author, ISBN, etc.) so the database is non-empty for demos.

Those example rows refer to **real, published works**. Metadata such as title, author, and ISBN are commonly reproduced under **fair dealing / fair use** for **academic citation and non-commercial coursework**, provided you:

- do **not** redistribute full copyrighted text from those books, and  
- **cite** the works in your technical report if your module expects bibliographic references.

Recommended citation style (adapt to your module’s Harvard/IEEE/etc. rules), e.g.:

- Thomas, D. and Hunt, A. (2019) *The Pragmatic Programmer: your journey to mastery* (20th Anniversary Edition). Boston: Addison-Wesley.  
- Kleppmann, M. (2017) *Designing Data-Intensive Applications*. Sebastopol: O’Reilly.  
- Martin, R.C. (2017) *Clean Architecture: A Craftsman’s Guide to Software Structure and Design*. Boston: Prentice Hall.

If you prefer to avoid citing real titles entirely, replace the seed rows with **fictional** metadata and state that clearly in your report.

## Third-party APIs

This coursework implementation **does not** call external book APIs at request time; it is a **self-contained** REST API over your own database.
