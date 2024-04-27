import json
from http import HTTPStatus

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_customers():
    response = client.get("/customers")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_create_customer():
    data = {"name": "John Doe", "email": "john.doe@example.com"}
    response = client.post("/customers", json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}


def test_get_customer_by_id():
    response = client.get("/customers/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}

    response = client.get("/customers/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Customer not found"}


def test_update_customer():
    data = {"name": "Jane Smith", "email": "jane.smith@example.com"}
    response = client.put("/customers/1", json=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "Jane Smith", "email": "jane.smith@example.com"}

    response = client.put("/customers/999", json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Customer not found"}


def test_delete_customer():
    response = client.delete("/customers/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Customer deleted successfully"}

    response = client.delete("/customers/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Customer not found"}