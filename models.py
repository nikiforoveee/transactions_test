import os

from gino import Gino

db = Gino()
# DB_URI = 'postgres://postgres:postgrespw@localhost:32775'
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

DB_URI = 'postgresql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(DB_PORT) + '/' + DB_NAME


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
    uid = db.Column(db.String(), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
