from flask import Blueprint

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from core_bank.models.user_model import User

account_bp = Blueprint(
    "account",
    __name__
)


@account_bp.route(
    "/account",
    methods=["GET"]
)
@jwt_required()
def account():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get(user_id)

    if not user:

        return {
            "status": "error",
            "message": "user_not_found"
        }, 404

    return {
        "status": "success",
        "account": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "balance": user.balance
        }
    }, 200
