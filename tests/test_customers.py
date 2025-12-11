from http import HTTPStatus

from app.extensions import db
from app.models import Customer

def test_get_all_customers_empty(client):
    response = client.get("/customers")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data == []


def test_get_customers_with_query_param(client, sample_customer):
    response = client.get("/customers?category=A")
    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert len(data) == 1
    assert data[0]["category"] == "A"


def test_create_customer_success(client):
    payload = {
        "name": "Juan",
        "lastname": "Perez",
        "category": "A",
        "age": 30,
        "email": "juan.perez@example.com",
        "url": "https://example.com",
        "birthday": "1990-01-01",
    }

    response = client.post("/customers", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data["id"] is not None


def test_create_customer_validation_error(client):
    payload = {
        "name": "Juan",
        "lastname": "Perez",
        "category": "A",
        "age": 30,
        "email": "no-es-un-email",
        "url": "https://example.com",
        "birthday": "1990-01-01",
    }

    response = client.post("/customers", json=payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_customer_by_id(client, sample_customer):
    response = client.get(f"/customers/{sample_customer.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["id"] == sample_customer.id
    assert data["email"] == sample_customer.email


def test_update_customer(client, sample_customer):
    payload = {
        "name": "Carlos",
        "age": 35,
    }

    response = client.put(f"/customers/{sample_customer.id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["name"] == "Carlos"
    assert data["age"] == 35


def test_delete_customer(client, sample_customer, app):
    response = client.delete(f"/customers/{sample_customer.id}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    with app.app_context():
        customer = db.session.get(Customer, sample_customer.id)
        assert customer is None
