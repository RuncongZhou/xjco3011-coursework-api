"""Load sample rows into the SQLite database (run from project root)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import select  # noqa: E402

from app.database import SessionLocal, engine  # noqa: E402
from app.database import Base  # noqa: E402
from app import models  # noqa: E402


SAMPLES = [
    {
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "isbn": "978-0135957059",
        "publication_year": 2019,
        "genre": "Technology",
        "pages": 352,
        "rating": 9.2,
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "isbn": "978-1449373320",
        "publication_year": 2017,
        "genre": "Technology",
        "pages": 616,
        "rating": 9.5,
    },
    {
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "isbn": "978-0134494166",
        "publication_year": 2017,
        "genre": "Technology",
        "pages": 432,
        "rating": 8.8,
    },
]


def main() -> None:
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for row in SAMPLES:
            exists = db.scalar(select(models.Book.id).where(models.Book.isbn == row["isbn"]))
            if exists:
                continue
            db.add(models.Book(**row))
        db.commit()
        print(f"Seeded {len(SAMPLES)} books (skipped existing ISBNs).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
