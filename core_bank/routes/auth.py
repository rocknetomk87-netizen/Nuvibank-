from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import random

from core_bank.core_app import db
from core_bank.models.user import User
from core_bank.models.account import Account

auth_bp = Blueprint("auth", __name__)


def generate_account_number():
    return str(random.randint(100000000000, 999999999999))


@auth_bp.route("/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    account = Account(
        user_id=new_user.id,
        account_number=generate_account_number(),
        balance=0.0,
        currency="USD",
        status="ACTIVE"
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        },
        "account": {
            "account_number": account.account_number,
            "balance": account.balance,
            "currency": account.currency,
            "status": account.status
        }
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })


@auth_bp.route("/auth/profile/<int:user_id>", methods=["GET"])
def profile(user_id):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    try:

        token = auth_header.split(" ")[1]

        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 401
