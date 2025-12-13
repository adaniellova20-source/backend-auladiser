import os
from datetime import date

import pytest
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.models import Customer

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_SESSION_OPTIONS"] = {"expire_on_commit": False}

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()

@pytest.fixture()
def sample_customer(app):
    customer = Customer(
        name="Juan",
        lastname="Perez",
        category="A",
        email="juan.perez@example.com",
        age=30,
        url="https://example.com",
        birthday=date(1997, 5, 10),
    )
    db.session.add(customer)
    db.session.commit()
    return customer
