from flask import Blueprint, jsonify, request
import jwt

from core_bank.models.account import Account
from core_bank.extensions import db
from core_bank.config import SECRET_KEY


wallet_bp = Blueprint(
    "wallet",
    __name__
)


def verify_token(req):

    auth_header = req.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        parts = auth_header.split()

        if len(parts) != 2:
            return None

        token = parts[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return decoded

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None



@wallet_bp.route(
    "/wallet/create",
    methods=["POST"]
)
def create_wallet():

    decoded = verify_token(request)

    if not decoded:
        return jsonify({
            "error": "Invalid token"
        }), 401


    existing = Account.query.filter_by(
        user_id=decoded["user_id"]
    ).first()


    if existing:
        return jsonify({
            "message": "Wallet already exists",
            "wallet": existing.to_dict()
        })


    wallet = Account(
        user_id=decoded["user_id"],
        balance=0.0
    )


    db.session.add(wallet)
    db.session.commit()


    return jsonify({
        "message": "Wallet created",
        "wallet": wallet.to_dict()
    }), 201



@wallet_bp.route(
    "/wallet/balance",
    methods=["GET"]
)
def balance():

    decoded = verify_token(request)

    if not decoded:
        return jsonify({
            "error": "Invalid token"
        }), 401


    wallet = Account.query.filter_by(
        user_id=decoded["user_id"]
    ).first()


    if not wallet:
        return jsonify({
            "error": "Wallet not found"
        }), 404


    return jsonify({
        "balance": str(wallet.balance),
        "currency": wallet.currency
    })
