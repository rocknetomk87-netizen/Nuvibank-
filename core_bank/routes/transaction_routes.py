from flask import Blueprint
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from core_bank.extensions.extensions import db

from core_bank.models.user_model import User
from core_bank.models.transaction_model import Transaction

transaction_bp = Blueprint(
    "transactions",
    __name__
)


@transaction_bp.route(
    "/deposit",
    methods=["POST"]
)
@jwt_required()
def deposit():

    data = request.get_json()

    amount = float(
        data.get("amount", 0)
    )

    if amount <= 0:

        return {
            "status": "error",
            "message": "invalid_amount"
        }, 400

    user_id = int(
        get_jwt_identity()
    )

    claims = get_jwt()

    user_email = claims.get("email")

    user = User.query.get(user_id)

    if not user:

        return {
            "status": "error",
            "message": "user_not_found"
        }, 404

    user.balance += amount

    transaction = Transaction(
        user_id=user.id,
        user_email=user_email,
        type="deposit",
        amount=amount
    )

    db.session.add(transaction)

    db.session.commit()

    return {
        "status": "success",
        "balance": user.balance
    }, 200


@transaction_bp.route(
    "/transfer",
    methods=["POST"]
)
@jwt_required()
def transfer():

    data = request.get_json()

    receiver_email = data.get("to")

    amount = float(
        data.get("amount", 0)
    )

    if amount <= 0:

        return {
            "status": "error",
            "message": "invalid_amount"
        }, 400

    sender_id = int(
        get_jwt_identity()
    )

    sender_claims = get_jwt()

    sender_email = sender_claims.get("email")

    sender = User.query.get(sender_id)

    receiver = User.query.filter_by(
        email=receiver_email
    ).first()

    if not sender or not receiver:

        return {
            "status": "error",
            "message": "user_not_found"
        }, 404

    if sender.balance < amount:

        return {
            "status": "error",
            "message": "insufficient_balance"
        }, 400

    sender.balance -= amount

    receiver.balance += amount

    sender_transaction = Transaction(
        user_id=sender.id,
        user_email=sender.email,
        type="transfer_sent",
        amount=amount
    )

    receiver_transaction = Transaction(
        user_id=receiver.id,
        user_email=receiver.email,
        type="transfer_received",
        amount=amount
    )

    db.session.add(sender_transaction)

    db.session.add(receiver_transaction)

    db.session.commit()

    return {
        "status": "success",
        "message": "transfer_completed",
        "balance": sender.balance
    }, 200


@transaction_bp.route(
    "/transactions",
    methods=["GET"]
)
@jwt_required()
def transactions():

    user_id = int(
        get_jwt_identity()
    )

    transactions = Transaction.query.filter_by(
        user_id=user_id
    ).order_by(
        Transaction.id.desc()
    ).all()

    data = []

    for transaction in transactions:

        data.append({
            "id": transaction.id,
            "type": transaction.type,
            "amount": transaction.amount,
            "user_email": transaction.user_email,
            "created_at": str(transaction.created_at)
        })

    return {
        "status": "success",
        "transactions": data
    }, 200
