from functools import wraps
from flask import request, jsonify

from security.jwt_handler import verify_token


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:

            return jsonify({
                "error": "Token não fornecido"
            }), 401

        data = verify_token(token)

        if not data:

            return jsonify({
                "error": "Token inválido"
            }), 401

        request.user = data

        return f(*args, **kwargs)

    return decorated


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:

            return jsonify({
                "error": "Token não fornecido"
            }), 401

        data = verify_token(token)

        if not data:

            return jsonify({
                "error": "Token inválido"
            }), 401

        if data["role"] != "admin":

            return jsonify({
                "error": "Acesso negado"
            }), 403

        request.user = data

        return f(*args, **kwargs)

    return decorated
