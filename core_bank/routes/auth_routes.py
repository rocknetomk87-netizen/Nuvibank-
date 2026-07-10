from flask import Blueprint
from flask import request

from flask_jwt_extended import create_access_token

from core_bank.extensions.extensions import (
    db,
    bcrypt
)

from core_bank.models.user_model import User

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:

        return {
            "status": "error",
            "message": "missing_fields"
        }, 400

    existing_user = User.query.filter(
        (
            User.email == email
        ) |
        (
            User.username == username
        )
    ).first()

    if existing_user:

        return {
            "status": "error",
            "message": "user_exists"
        }, 409

    password_hash = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)

    db.session.commit()

    return {
        "status": "success",
        "message": "user_created"
    }, 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return {
            "status": "error",
            "message": "missing_credentials"
        }, 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        return {
            "status": "error",
            "message": "invalid_credentials"
        }, 401

    password_valid = bcrypt.check_password_hash(
        user.password_hash,
        password
    )

    if not password_valid:

        return {
            "status": "error",
            "message": "invalid_credentials"
        }, 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email
        }
    )

    return {
        "status": "success",
        "token": token
    }, 200
