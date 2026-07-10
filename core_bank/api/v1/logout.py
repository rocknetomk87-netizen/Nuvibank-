from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from core_bank.security.token_blacklist import (
    add_token_to_blacklist
)

logout_api = Blueprint(
    "logout_api",
    __name__
)

@logout_api.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():

    jti = get_jwt()["jti"]

    add_token_to_blacklist(jti)

    return jsonify({
        "status": "success",
        "message": "logged_out"
    }), 200
