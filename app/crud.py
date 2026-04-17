from sqlalchemy import and_, asc, desc, func, or_, select
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


def _book_filters(
    genre: str | None,
    author: str | None,
    q: str | None,
):
    conditions = []
    if genre:
        conditions.append(models.Book.genre == genre)
    if author:
        conditions.append(models.Book.author.ilike(f"%{author}%"))
    if q and q.strip():
        term = f"%{q.strip()}%"
        conditions.append(
            or_(
                models.Book.title.ilike(term),
                models.Book.author.ilike(term),
                models.Book.isbn.ilike(term),
            )
        )
    return conditions


def count_books(
    db: Session,
    *,
    genre: str | None = None,
    author: str | None = None,
    q: str | None = None,
) -> int:
    stmt = select(func.count()).select_from(models.Book)
    conds = _book_filters(genre, author, q)
    if conds:
        stmt = stmt.where(and_(*conds))
    return int(db.scalar(stmt) or 0)


def get_books(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    genre: str | None = None,
    author: str | None = None,
    q: str | None = None,
    sort: schemas.SortField = schemas.SortField.created_at,
    order: schemas.SortOrder = schemas.SortOrder.desc,
) -> tuple[list[models.Book], int]:
    total = count_books(db, genre=genre, author=author, q=q)
    stmt = select(models.Book)
    conds = _book_filters(genre, author, q)
    if conds:
        stmt = stmt.where(and_(*conds))

    col = getattr(models.Book, sort.value)
    stmt = stmt.order_by(desc(col) if order == schemas.SortOrder.desc else asc(col))
    stmt = stmt.offset(skip).limit(min(limit, 100))
    rows = list(db.scalars(stmt).all())
    return rows, total


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
