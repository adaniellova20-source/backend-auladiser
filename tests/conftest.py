from datetime import date

from pytest import fixture
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.config import  ConfigTest
from app.models import Customer

@fixture()
def app():
    app = create_app(ConfigTest)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()

@fixture()
def client(app) -> FlaskClient:
    return app.test_client()

@fixture()
def sample_customer(app):
    customer = Customer(
        name="Juan",
        lastname="Perez",
        category="A",
        email="juan.perez@example.com",
        age=30,
        url="https://example.com",
        birthday=date(1998, 5, 10),
    )
    db.session.add(customer)
    db.session.commit()
    return customer
