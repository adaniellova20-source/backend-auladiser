from app.routes.customers import customers_bp

def register_routes(app):
    app.register_blueprint(customers_bp)
