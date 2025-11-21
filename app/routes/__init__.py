from app.routes.customers import customers_bp
from app.routes.auth import auth_bp

def register_routes(app):
    app.register_blueprint(customers_bp)
    app.register_blueprint(auth_bp)
