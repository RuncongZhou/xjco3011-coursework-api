from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=300)
    isbn: str | None = Field(None, max_length=20)
    publication_year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, max_length=120)
    pages: int | None = Field(None, ge=0)
    rating: float | None = Field(None, ge=0, le=10)
    notes: str | None = None


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


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None


class Message(BaseModel):
    detail: str


class BookStats(BaseModel):
    total_books: int
    average_rating: float | None
    genres: dict[str, int]
