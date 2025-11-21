from http import HTTPStatus
import os

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from dotenv import load_dotenv

from flask_jwt_extended import create_access_token

from app.schemas import UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()

load_dotenv()

@auth_bp.post('/login')
def get_token():
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST

    env_user = os.getenv('USER')
    env_password = os.getenv('PASSWORD')

    if env_user != data['username'] or env_password != data['password']:
        return jsonify({"message": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED

    token = create_access_token(identity=data['username'])
    return token, HTTPStatus.OK
