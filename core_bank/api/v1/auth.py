from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_api = Blueprint("auth_api", __name__)

fake_users = {
    "ceo@nuvibank.com": {
        "id": 1,
        "password": "UltraSecure123"
    }
}

@auth_api.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = fake_users.get(email)

    if not user:
        return jsonify({
            "status": "error",
            "message": "user_not_found"
        }), 404

    if user["password"] != password:
        return jsonify({
            "status": "error",
            "message": "invalid_credentials"
        }), 401

    token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "status": "success",
        "access_token": token
    }), 200
