from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Missing credentials"}), HTTPStatus.BAD_REQUEST

    user = User.query.filter(User.username == auth.username).first()

    if not user or not user.check_password(auth.password):
        return jsonify({"message": "Invalid credentials"}), HTTPStatus.UNAUTHORIZED

    token = create_access_token(identity=user.id)

    return jsonify({"access_token": token}), HTTPStatus.OK
