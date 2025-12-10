from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db
from app.models import Customer
from app.schemas import CustomerSchema

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customers_bp.get('')
def get_all_customers():
    """
    Obtener todos los clientes o filtrarlos por parámetros de consulta.
    ---
    tags:
      - Customers
    parameters:
      - in: query
        name: name
        type: string
        required: false
        description: Filtrar por nombre.
      - in: query
        name: lastname
        type: string
        required: false
        description: Filtrar por apellido.
      - in: query
        name: category
        type: string
        required: false
        enum: ["A", "B", "C"]
        description: Filtrar por categoría.
      - in: query
        name: email
        type: string
        required: false
        description: Filtrar por correo electrónico.
      - in: query
        name: age
        type: integer
        required: false
        description: Filtrar por edad.
      - in: query
        name: is_active
        type: boolean
        required: false
        description: Filtrar por estado activo.

    definitions:
      Customer:
        type: object
        properties:
          id:
            type: integer
            readOnly: true
            example: 1
          name:
            type: string
            example: Angel
          lastname:
            type: string
            example: Lopez Vazquez
          category:
            type: string
            enum: ["A", "B", "C"]
            example: "A"
          email:
            type: string
            format: email
            example: "angel@example.com"
          age:
            type: integer
            example: 30
          url:
            type: string
            format: url
            example: "https://auladiser.com"
          birthday:
            type: string
            format: date
            example: "1995-05-10"
          created_at:
            type: string
            format: date-time
            readOnly: true
          updated_at:
            type: string
            format: date-time
            readOnly: true
          is_active:
            type: boolean
            example: true
        required:
          - name
          - lastname
          - email
          - url
          - birthday

    responses:
      200:
        description: Lista de clientes
        schema:
          type: array
          items:
            $ref: '#/definitions/Customer'
    """
    if request.args:
        customers = Customer.query.filter_by(**request.args)
    else:
        customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), HTTPStatus.OK


@customers_bp.get('/<int:id>')
def get_customer_by_id(id):
    """
    Obtener un cliente por su identificador.
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del cliente.
    responses:
      200:
        description: Cliente encontrado
        schema:
          $ref: '#/definitions/Customer'
      404:
        description: Cliente no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    return jsonify(customer_schema.dump(customer)), HTTPStatus.OK


@customers_bp.post('')
def create_customer():
    """
    Crear un nuevo cliente.
    ---
    tags:
      - Customers
    parameters:
      - in: body
        name: body
        description: Datos del cliente a crear.
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Angel
            lastname:
              type: string
              example: Lopez Vazquez
            category:
              type: string
              enum: ["A", "B", "C"]
              example: "A"
            email:
              type: string
              format: email
              example: "angel@example.com"
            age:
              type: integer
              example: 30
            url:
              type: string
              format: url
              example: "https://auladiser.com"
            birthday:
              type: string
              format: date
              example: "1995-05-10"
            is_active:
              type: boolean
              example: true
          required:
            - name
            - lastname
            - email
            - url
            - birthday
    responses:
      201:
        description: Cliente creado exitosamente
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Error de validación en los datos enviados
        schema:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          example:
            email:
              - "El formato del correo no es válido."
    """
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
    """
    Actualizar parcialmente un cliente existente.
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del cliente a actualizar.
      - in: body
        name: body
        description: Datos del cliente a actualizar (parcialmente).
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Angel
            lastname:
              type: string
              example: Lopez Vazquez
            category:
              type: string
              enum: ["A", "B", "C"]
              example: "B"
            email:
              type: string
              format: email
            age:
              type: integer
            url:
              type: string
              format: url
            birthday:
              type: string
              format: date
            is_active:
              type: boolean
    responses:
      200:
        description: Cliente actualizado exitosamente
        schema:
          $ref: '#/definitions/Customer'
      400:
        description: Error de validación en los datos enviados
        schema:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
      404:
        description: Cliente no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
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
    """
    Eliminar un cliente por su identificador.
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del cliente a eliminar.
    responses:
      204:
        description: Cliente eliminado exitosamente (sin contenido en la respuesta).
      404:
        description: Cliente no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify(), HTTPStatus.NO_CONTENT


@customers_bp.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    """
    Manejo de error cuando un cliente no es encontrado.
    ---
    tags:
      - Customers
    responses:
      404:
        description: Cliente no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Customer not found
    """
    return jsonify({"error": "Customer not found"}), HTTPStatus.NOT_FOUND
