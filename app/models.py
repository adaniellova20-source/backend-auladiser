from app.extensions import db, bcrypt

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

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError("La contraseña no se puede leer.")

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password_hash, plaintext_password)
