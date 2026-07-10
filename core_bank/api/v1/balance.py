from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core_bank.api.v1.deposit import fake_balances

balance_api = Blueprint("balance_api", __name__)

@balance_api.route("/balance", methods=["GET"])
@jwt_required()
def balance():

    user_id = get_jwt_identity()

    balance = fake_balances.get(user_id, 0)

    return jsonify({
        "status": "success",
        "balance": balance
    }), 200
