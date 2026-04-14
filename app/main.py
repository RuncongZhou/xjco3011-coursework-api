from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import books


@asynccontextmanager
async def lifespan(_: FastAPI):
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "REST API for managing a book catalogue (CRUD + analytics). "
        "Coursework for XJCO3011 Web Services and Web Data."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/api/v1")


@app.get("/", tags=["meta"])
def root():
    return {
        "service": settings.app_name,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "api_base": "/api/v1",
    }


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
