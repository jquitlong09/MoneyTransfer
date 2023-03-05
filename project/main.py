from flask import Blueprint, request, make_response
from . import db
from .models import User, Audit, Transaction
from flask_login import login_required, current_user
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/profile', methods=['GET'])
@cross_origin()
@jwt_required()
def profile():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    details = {}
    details["email"] = user.email
    details["name"] = user.name
    details["balance"] = user.balance if user.balance is not None else float(0)
    return details

@main.route('/send-to-bank', methods=['POST'])
@cross_origin()
@jwt_required()
def send_to_bank():
    bank = request.form.get('bank')
    amount = request.form.get('amount')
    notes = request.form.get('notes')
    account_name = request.form.get('account_name')
    account_number = request.form.get('account_number')
    
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    current_bal = current_user.balance if current_user.balance is not None else 0
    if float(current_bal) < float(amount):
        return "Insufficient balance", 404
    
    # Sending user
    sender = User.query.filter_by(email=current_user.email).first()
    snd_balance = sender.balance if sender.balance is not None else float(0)
    snd_balance -= float(amount)
    sender.balance = snd_balance
    db.session.commit()


    # Save Transaction Sender
    transaction_type = "SEND_TO_BANK"
    adjustment = float(amount) * -1
    prev_balance = sender.balance if sender.balance is not None else float(0)
    curr_balance = snd_balance
    sender_id = sender.id
    txn = Transaction(prev_balance=prev_balance, adjustment=adjustment,
                      sender_id=sender_id, transaction_type=transaction_type,
                      notes=notes, curr_balance=curr_balance, bank=bank,
                      account_number=account_number, account_name=account_name)
    db.session.add(txn)
    db.session.commit()
    
    return "OK"

@main.route('/send-to-user', methods=['POST'])
@cross_origin()
@jwt_required()
def send_to_user():
    email = request.form.get('email')
    amount = request.form.get('amount')
    notes = request.form.get('notes')
    
    user = User.query.filter_by(email=email).first()
    print("user ", user)
    if user is None:
        return "User does not exist", 404
    
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    current_bal = current_user.balance if current_user.balance is not None else 0
    if float(current_bal) < float(amount):
        return "Insufficient balance", 404
    
    # Receiving user
    rcv_balance = user.balance if user.balance is not None else float(0)
    rcv_balance += float(amount)
    user.balance = rcv_balance
    db.session.commit()
    
    # Sending user
    sender = User.query.filter_by(email=current_user.email).first()
    snd_balance = sender.balance if sender.balance is not None else float(0)
    snd_balance -= float(amount)
    sender.balance = snd_balance
    db.session.commit()

    audit = Audit(action="User sends money amounting to " + amount, user_id=user.id)
    db.session.add(audit)
    db.session.commit()
    
    # Save Transaction Sender
    transaction_type = "SEND_TO_USER"
    adjustment = float(amount) * -1
    prev_balance = sender.balance if sender.balance is not None else float(0)
    curr_balance = snd_balance
    sender_id = sender.id
    txn = Transaction(prev_balance=prev_balance, adjustment=adjustment,
                      sender_id=sender_id, transaction_type=transaction_type,
                      notes=notes, curr_balance=curr_balance)
    db.session.add(txn)
    db.session.commit()
    
    # Save Transaction Receiver
    transaction_type = "SEND_TO_USER"
    adjustment = float(amount)
    prev_balance =  user.balance if user.balance is not None else float(0)
    curr_balance = rcv_balance
    sender_id = user.id
    txn = Transaction(prev_balance=prev_balance, adjustment=adjustment,
                      sender_id=sender_id, transaction_type=transaction_type,
                      notes=notes, curr_balance=curr_balance)
    db.session.add(txn)
    db.session.commit()
    
    return "OK"

@main.route('/admin-topup', methods=['POST'])
@login_required
def admin_topup():
    email = request.form.get('email')
    amount = request.form.get('amount')
    
    if current_user.email != "admin@yopmail.com":
        return "Insufficient permission"

    # Receiving user
    user = User.query.filter_by(email=email).first()
    rcv_balance = user.balance if user.balance is not None else float(0)
    rcv_balance += float(amount)
    user.balance = rcv_balance
    db.session.commit()
    
    return "Success topup"

@main.route('/audit', methods=['GET'])
@cross_origin()
@jwt_required()
def audit():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    audit = Audit.query.filter_by(user_id=current_user.id).all()
    audits = []
    for item in audit:
        data = {}
        data["action"] = item.action
        audits.append(data)
    return audits

@main.route('/transaction', methods=['GET'])
@cross_origin()
@jwt_required()
def transaction():
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    txn = Transaction.query.filter_by(sender_id=current_user.id).all()
    txns = []
    for item in txn:
        data = {}
        data["prev_balance"] = item.prev_balance
        data["adjustment"] = item.adjustment
        data["transaction_type"] = item.transaction_type
        data["notes"] = item.notes
        data["curr_balance"] = item.curr_balance
        txns.append(data)
    return txns