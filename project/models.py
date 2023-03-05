from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    balance = db.Column(db.Float)
    audits = db.relationship('Audit', backref='user')
    transactions_sender = db.relationship('Transaction', backref='user')

class Audit(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
class Transaction(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prev_balance = db.Column(db.Float)
    curr_balance = db.Column(db.Float)
    adjustment = db.Column(db.Float)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_number = db.Column(db.String(100))
    account_name = db.Column(db.String(100))
    transaction_type = db.Column(db.String(100))
    notes = db.Column(db.String(1000))
    bank = db.Column(db.String(1000))

class Provider(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    banks = db.relationship('Bank', backref='provider')

class Bank(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
