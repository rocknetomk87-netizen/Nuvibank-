from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

deposit_api = Blueprint("deposit_api", __name__)

fake_balances = {}

@deposit_api.route("/deposit", methods=["POST"])
@jwt_required()
def deposit():

    user_id = get_jwt_identity()

    data = request.get_json()

    amount = float(data.get("amount", 0))

    current_balance = fake_balances.get(user_id, 0)

    new_balance = current_balance + amount

    fake_balances[user_id] = new_balance

    return jsonify({
        "status": "success",
        "balance": new_balance
    }), 200
