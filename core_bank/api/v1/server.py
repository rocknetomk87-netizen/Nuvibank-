from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from core_bank.extensions import db, limiter
from core_bank.models.user import User
from core_bank.models.transaction import Transaction

api = Blueprint("api", __name__)


# =========================
# REGISTER
# =========================
@api.post("/register")
@limiter.limit("5 per minute")
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "status": "error",
            "message": "missing_fields"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "status": "error",
            "message": "user_exists"
        }), 409

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "user_created"
    }), 201


# =========================
# LOGIN
# =========================
@api.post("/login")
@limiter.limit("5 per minute")
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "missing_credentials"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "status": "error",
            "message": "invalid_credentials"
        }), 401

    if not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "invalid_credentials"
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "status": "success",
        "access_token": token
    }), 200


# =========================
# BALANCE
# =========================
@api.get("/balance")
@jwt_required()
def balance():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "status": "error",
            "message": "user_not_found"
        }), 404

    return jsonify({
        "status": "success",
        "balance": float(user.balance)
    }), 200


# =========================
# DEPOSIT
# =========================
@api.post("/deposit")
@jwt_required()
def deposit():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "status": "error",
            "message": "user_not_found"
        }), 404

    data = request.get_json()

    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({
            "status": "error",
            "message": "invalid_amount"
        }), 400

    user.balance += amount

    transaction = Transaction(
        user_id=user.id,
        type="deposit",
        amount=amount,
        description="Balance deposit"
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "status": "success",
        "balance": float(user.balance)
    }), 200


# =========================
# TRANSFER
# =========================
@api.post("/transfer")
@jwt_required()
def transfer():

    sender_id = get_jwt_identity()

    sender = User.query.get(sender_id)

    if not sender:
        return jsonify({
            "status": "error",
            "message": "sender_not_found"
        }), 404

    data = request.get_json()

    receiver_email = data.get("to")
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({
            "status": "error",
            "message": "invalid_amount"
        }), 400

    receiver = User.query.filter_by(email=receiver_email).first()

    if not receiver:
        return jsonify({
            "status": "error",
            "message": "receiver_not_found"
        }), 404

    if sender.balance < amount:
        return jsonify({
            "status": "error",
            "message": "insufficient_balance"
        }), 400

    sender.balance -= amount
    receiver.balance += amount

    sender_transaction = Transaction(
        user_id=sender.id,
        type="transfer_out",
        amount=amount,
        description=f"Transfer to {receiver.email}"
    )

    receiver_transaction = Transaction(
        user_id=receiver.id,
        type="transfer_in",
        amount=amount,
        description=f"Transfer from {sender.email}"
    )

    db.session.add(sender_transaction)
    db.session.add(receiver_transaction)

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "transfer_completed",
        "sender_balance": float(sender.balance)
    }), 200


# =========================
# TRANSACTIONS
# =========================
@api.get("/transactions")
@jwt_required()
def transactions():

    user_id = get_jwt_identity()

    transactions = Transaction.query.filter_by(
        user_id=user_id
    ).order_by(
        Transaction.created_at.desc()
    ).all()

    data = []

    for tx in transactions:
        data.append({
            "id": tx.id,
            "type": tx.type,
            "amount": float(tx.amount),
            "description": tx.description,
            "created_at": str(tx.created_at)
        })

    return jsonify({
        "status": "success",
        "transactions": data
    }), 200
