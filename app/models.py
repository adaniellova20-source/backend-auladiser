from app.extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
