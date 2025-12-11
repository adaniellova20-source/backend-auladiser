import os
from datetime import date

import pytest
from flask.testing import FlaskClient

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from app import create_app
from app.extensions import db
from app.models import Customer


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_SESSION_OPTIONS={
            "expire_on_commit": False
        }
    )

    # mantenemos el app_context vivo durante todo el test
    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    ctx.pop()


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
