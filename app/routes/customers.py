from http import HTTPStatus

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from app.models import db, Customer
from app.schemas import CustomerSchema

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

schema = CustomerSchema()
schemas = CustomerSchema(many=True)

@customers_bp.get('/')
def get_all_customers():
    if len(request.args) == 0:
        customers = Customer.query.all()
    else:
        customers = Customer.query.filter_by(**request.args).all()
    return jsonify(schemas.dump(customers))

@customers_bp.get('/<int:id>')
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(schema.dump(customer)), HTTPStatus.OK

@customers_bp.post('')
@jwt_required()
def create_customer():
    try:
        data = schema.load(request.get_json())
        existing = Customer.query.filter_by(email=data["email"]).first()
        if existing:
            return jsonify({"error": "Email already exists"}), HTTPStatus.CONFLICT
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify(schema.dump(customer)), HTTPStatus.CREATED

@customers_bp.put("/<int:id>")
@jwt_required()
def update_customer(id):
    try:
        data = schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    if "email" in data:
        existing = Customer.query.filter(Customer.email == data["email"],Customer.id != id).first()
        if existing:
            return jsonify({"error": "Email already exists"}), HTTPStatus.CONFLICT

    customer = Customer.query.get_or_404(id)

    customer.name = data.get('name', customer.name)
    customer.lastname = data.get('lastname', customer.lastname)
    customer.category = data.get('category', customer.category)
    customer.email = data.get('email', customer.email)
    customer.age = data.get('age', customer.age)
    customer.url = data.get('url', customer.url)
    customer.birthday = data.get('birthday', customer.birthday)

    db.session.commit()
    return jsonify(schema.dump(customer)), HTTPStatus.OK

@customers_bp.patch('/<int:id>/activate')
@jwt_required()
def activate_customer(id):
    customer = Customer.query.get_or_404(id)
    if not customer.is_active:
        customer.is_active = True
        db.session.commit()
        return jsonify(), HTTPStatus.OK
    else:
        return jsonify(), HTTPStatus.NOT_MODIFIED

@customers_bp.patch('/<int:id>/desactivate')
@jwt_required()
def desactivate_customer(id):
    customer = Customer.query.get_or_404(id)
    if customer.is_active:
        customer.is_active = False
        db.session.commit()
        return jsonify(), HTTPStatus.OK
    else:
        return jsonify(), HTTPStatus.NOT_MODIFIED

@customers_bp.delete("/<int:id>")
@jwt_required()
def delete_user(id: int):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify(), HTTPStatus.NO_CONTENT

@customers_bp.errorhandler(HTTPStatus.NOT_FOUND)
def not_found():
    return jsonify({"error": "Customer not found"}), HTTPStatus.NOT_FOUND