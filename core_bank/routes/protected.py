from flask import Blueprint, jsonify, request

import jwt

from core_bank.config import SECRET_KEY


protected_bp = Blueprint(
    "protected",
    __name__
)


@protected_bp.route(
    "/protected",
    methods=["GET"]
)
def protected():

    token = request.headers.get(
        "Authorization"
    )


    if not token:

        return jsonify({
            "error": "missing_token"
        }), 401


    try:

        token = token.replace(
            "Bearer ",
            ""
        )


        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )


        return jsonify({

            "message": "Access granted",

            "user": decoded

        })


    except jwt.ExpiredSignatureError:

        return jsonify({

            "error": "token_expired"

        }), 401


    except jwt.InvalidTokenError:

        return jsonify({

            "error": "invalid_token"

        }), 401
