from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db
from app.routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    app.url_map.strict_slashes = False

    register_routes(app)

    return app
