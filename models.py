from gino import Gino

db = Gino()
DB_URI = 'postgres://postgres:postgrespw@localhost:32775'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    balance = db.Column(db.Numeric(precision=10, scale=2))


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    current_balance = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    uid = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
