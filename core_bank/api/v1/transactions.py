from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

transactions_api = Blueprint("transactions_api", __name__)

@transactions_api.route("/transactions", methods=["GET"])
@jwt_required()
def transactions():

    return jsonify({
        "status": "success",
        "transactions": [
            {
                "type": "deposit",
                "amount": 250000
            }
        ]
    }), 200
