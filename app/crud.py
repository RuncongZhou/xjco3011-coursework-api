from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    row = models.Book(**book.model_dump())
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(row)
    return row


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.get(models.Book, book_id)


def get_books(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    genre: str | None = None,
    author: str | None = None,
) -> list[models.Book]:
    stmt = select(models.Book).offset(skip).limit(min(limit, 100))
    if genre:
        stmt = stmt.where(models.Book.genre == genre)
    if author:
        stmt = stmt.where(models.Book.author.ilike(f"%{author}%"))
    return list(db.scalars(stmt).all())


def update_book(db: Session, book_id: int, data: schemas.BookUpdate) -> models.Book | None:
    row = db.get(models.Book, book_id)
    if not row:
        return None
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(row, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(row)
    return row


def delete_book(db: Session, book_id: int) -> bool:
    row = db.get(models.Book, book_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True


def book_stats(db: Session) -> schemas.BookStats:
    total = db.scalar(select(func.count()).select_from(models.Book)) or 0
    avg = db.scalar(select(func.avg(models.Book.rating)).where(models.Book.rating.isnot(None)))
    genres: dict[str, int] = {}
    rows = db.execute(
        select(models.Book.genre, func.count())
        .where(models.Book.genre.isnot(None))
        .group_by(models.Book.genre)
    ).all()
    for g, c in rows:
        if g:
            genres[g] = int(c)
    return schemas.BookStats(
        total_books=int(total),
        average_rating=float(avg) if avg is not None else None,
        genres=genres,
    )
