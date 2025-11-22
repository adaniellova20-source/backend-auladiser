from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, jwt
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    register_routes(app)

    return app
