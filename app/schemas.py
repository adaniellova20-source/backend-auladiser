from datetime import date
from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models import Customer

class CustomerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=[
            validate.Regexp('^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$', error="El nombre debe iniciar con mayúscula y contener solo letras."),
            validate.Length(min=3, error="El nombre debe tener al menos 3 caracteres."),
        ],
        error_messages={"required": "El nombre es obligatorio."}
    )
    lastname = fields.String(
        required=True,
        validate=[
            validate.Regexp('^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$', error="El apellido debe iniciar con mayúscula y contener solo letras."),
            validate.Length(min=3, error="El apellido debe tener al menos 3 caracteres."),
        ],
        error_messages={"required": "El apellido es obligatorio."}
    )
    category = fields.String(
        validate=validate.OneOf(["A", "B", "C"], error="La categoría debe ser A, B o C.")
    )
    email = fields.Email(
        required=True,
        validate=validate.Email(error="El formato del correo no es válido."),
        error_messages={
            "required": "El correo electrónico es obligatorio.",
            "invalid": "El formato del correo no es válido.",
        },
    )
    age = fields.Integer(
        validate=[
            validate.Range(min=1, max=100, error="La edad debe estar entre 1 y 100 años.")
        ]
    )
    url = fields.URL(
        required=True,
        error_messages={
            "required": "La URL es obligatoria.",
            "invalid": "El formato de la URL no es válido.",
        },
    )
    birthday = fields.Date(
        required=True,
        validate=validate.Range(max=date.today(), error="La fecha de nacimiento no puede ser futura."),
        error_messages={"required": "La fecha de nacimiento es obligatoria."},
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool()

    @validates("email")
    def validate_unique_email(self, value, **kwargs):
        exists = Customer.query.filter_by(email=value).first()
        if exists:
            raise ValidationError("Este correo ya está registrado.")

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
