"""Tests for the sandbox-os endpoints, against main.app with FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def reset_store():
    """Give every test an empty store, so tests are independent of order."""
    main._items.clear()
    main._next_id = 1
    yield
    main._items.clear()
    main._next_id = 1


@pytest.fixture
def client():
    return TestClient(main.app)


def create(client, name="widget", description=""):
    response = client.post("/items", json={"name": name, "description": description})
    assert response.status_code == 201
    return response.json()


# GET /health

def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# GET /items

def test_list_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_returns_created_items(client):
    first = create(client, "first")
    second = create(client, "second", "two")
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [first, second]


# GET /items/{id}

def test_get_item_returns_item(client):
    created = create(client, "widget", "a widget")
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "name": "widget", "description": "a widget"}


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


# POST /items

def test_create_item_returns_201_and_item(client):
    response = client.post("/items", json={"name": "widget", "description": "a widget"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "widget", "description": "a widget"}


def test_create_item_description_defaults_to_empty(client):
    response = client.post("/items", json={"name": "widget"})
    assert response.status_code == 201
    assert response.json()["description"] == ""


def test_create_item_ids_increase(client):
    ids = [create(client, f"item-{n}")["id"] for n in range(3)]
    assert ids == [1, 2, 3]


def test_create_item_without_name_is_rejected(client):
    response = client.post("/items", json={"description": "no name"})
    assert response.status_code == 422


# DELETE /items/{id}

def test_delete_item_removes_it(client):
    created = create(client)
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/items/{created['id']}").status_code == 404
    assert client.get("/items").json() == []


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
