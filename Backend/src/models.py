from Backend.src.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    cryptocurrency = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(20, 8), nullable=False)
    transaction_type = db.Column(db.String(4), nullable=False)
    transaction_price = db.Column(db.Numeric(20, 8), nullable=False)
    transaction_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PortfolioHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Numeric(20,8), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'value': self.value
        }