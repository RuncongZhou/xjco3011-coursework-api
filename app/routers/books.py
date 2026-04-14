from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.deps import require_write_key

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book",
    dependencies=[Depends(require_write_key)],
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.BookRead:
    try:
        return crud.create_book(db, book)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISBN already exists for another book.",
        ) from None


@router.get("/stats/summary", response_model=schemas.BookStats, summary="Aggregate statistics")
def book_statistics(db: Session = Depends(get_db)) -> schemas.BookStats:
    return crud.book_stats(db)


@router.get(
    "",
    response_model=schemas.BookListResponse,
    summary="List books (paginated)",
)
def list_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Page size (max 100)"),
    genre: str | None = Query(None, description="Exact genre filter"),
    author: str | None = Query(None, description="Partial author match (case-insensitive)"),
    q: str | None = Query(
        None,
        description="Search title, author, or ISBN (case-insensitive substring)",
        max_length=200,
    ),
    sort: schemas.SortField = Query(
        schemas.SortField.created_at,
        description="Field to sort by",
    ),
    order: schemas.SortOrder = Query(
        schemas.SortOrder.desc,
        description="Sort direction",
    ),
) -> schemas.BookListResponse:
    items, total = crud.get_books(
        db,
        skip=skip,
        limit=limit,
        genre=genre,
        author=author,
        q=q,
        sort=sort,
        order=order,
    )
    return schemas.BookListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{book_id}", response_model=schemas.BookRead, summary="Get one book by id")
def read_book(book_id: int, db: Session = Depends(get_db)) -> schemas.BookRead:
    row = crud.get_book(db, book_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return row


@router.patch(
    "/{book_id}",
    response_model=schemas.BookRead,
    summary="Update a book",
    dependencies=[Depends(require_write_key)],
)
def update_book(
    book_id: int,
    data: schemas.BookUpdate,
    db: Session = Depends(get_db),
) -> schemas.BookRead:
    try:
        row = crud.update_book(db, book_id, data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISBN already exists for another book.",
        ) from None
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return row


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    dependencies=[Depends(require_write_key)],
)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    if not crud.delete_book(db, book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
