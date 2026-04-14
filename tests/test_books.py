from fastapi.testclient import TestClient


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_crud_flow(client: TestClient):
    create = client.post(
        "/api/v1/books",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-0000000001",
            "publication_year": 2020,
            "genre": "Fiction",
            "pages": 300,
            "rating": 8.5,
        },
    )
    assert create.status_code == 201
    book_id = create.json()["id"]

    one = client.get(f"/api/v1/books/{book_id}")
    assert one.status_code == 200
    assert one.json()["title"] == "Test Book"

    upd = client.patch(
        f"/api/v1/books/{book_id}",
        json={"rating": 9.0, "notes": "Updated"},
    )
    assert upd.status_code == 200
    assert upd.json()["rating"] == 9.0

    lst = client.get("/api/v1/books")
    assert lst.status_code == 200
    assert len(lst.json()) == 1

    stats = client.get("/api/v1/books/stats/summary")
    assert stats.status_code == 200
    assert stats.json()["total_books"] == 1

    delete = client.delete(f"/api/v1/books/{book_id}")
    assert delete.status_code == 204

    missing = client.get(f"/api/v1/books/{book_id}")
    assert missing.status_code == 404


def test_duplicate_isbn_conflict(client: TestClient):
    payload = {
        "title": "A",
        "author": "B",
        "isbn": "978-dup",
    }
    assert client.post("/api/v1/books", json=payload).status_code == 201
    dup = client.post("/api/v1/books", json=payload)
    assert dup.status_code == 409
