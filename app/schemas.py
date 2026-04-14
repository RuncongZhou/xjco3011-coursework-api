from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=300)
    isbn: str | None = Field(None, max_length=20)
    publication_year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, max_length=120)
    pages: int | None = Field(None, ge=0)
    rating: float | None = Field(None, ge=0, le=10)
    notes: str | None = None

    @field_validator("isbn")
    @classmethod
    def strip_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip()
        return s or None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=300)
    isbn: str | None = Field(None, max_length=20)
    publication_year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, max_length=120)
    pages: int | None = Field(None, ge=0)
    rating: float | None = Field(None, ge=0, le=10)
    notes: str | None = None

    @field_validator("isbn")
    @classmethod
    def strip_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip()
        return s or None


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None


class BookListResponse(BaseModel):
    items: list[BookRead]
    total: int
    skip: int
    limit: int


class Message(BaseModel):
    detail: str


class BookStats(BaseModel):
    total_books: int
    average_rating: float | None
    genres: dict[str, int]


class SortField(str, Enum):
    created_at = "created_at"
    title = "title"
    rating = "rating"
    publication_year = "publication_year"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
