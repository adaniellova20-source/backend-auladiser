from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db
from app.models import Customer
from app.schemas import CustomerSchema

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

customer_schema = CustomerSchema()

@customers_bp.get('')
def get_all_customers():
    if request.args:
        try:
            filters = customer_schema.load(request.args, partial=True)
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        customers = Customer.query.filter_by(**filters).all()
    else:
        customers = Customer.query.all()
    return jsonify(customer_schema.dump(customers, many=True)), HTTPStatus.OK

@customers_bp.get('/<int:id>')
def get_customer_by_id(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer_schema.dump(customer)), HTTPStatus.OK

@customers_bp.post('')
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), HTTPStatus.BAD_REQUEST

    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer_schema.dump(customer)), HTTPStatus.CREATED

@customers_bp.put("/<int:id>")
def update_customer(id):
    try:
        data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), HTTPStatus.BAD_REQUEST

    customer = Customer.query.get_or_404(id)

    customer.name = data.get('name', customer.name)
    customer.lastname = data.get('lastname', customer.lastname)
    customer.category = data.get('category', customer.category)
    customer.email = data.get('email', customer.email)
    customer.age = data.get('age', customer.age)
    customer.url = data.get('url', customer.url)
    customer.birthday = data.get('birthday', customer.birthday)

    db.session.commit()
    return jsonify(customer_schema.dump(customer)), HTTPStatus.OK

@customers_bp.delete("/<int:id>")
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify(), HTTPStatus.NO_CONTENT

@customers_bp.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    return jsonify({"error": "Customer not found"}), HTTPStatus.NOT_FOUND
