from datetime import date

from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=[
            validate.Regexp('^[A-Z][a-z]+$'),
            validate.Length(min=3),
        ]
    )
    lastname = fields.String(
        required=True,
        validate=[
            validate.Regexp('^[A-Z][a-z]+$'),
            validate.Length(min=3),
        ]
    )
    category = fields.String(validate=validate.OneOf(["A", "B", "C"]))
    email = fields.Email(required=True, validate=validate.Email())
    age = fields.Integer(
        validate=[
            validate.Range(min=1, max=100)
        ]
    )
    url = fields.URL(required=True)
    birthday = fields.Date(required=True, validate=validate.Range(max=date.today()))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool()

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)