from flask import jsonify


def success_response(data=None, message="success"):

    response = {
        "status": "success",
        "message": message
    }

    if data:
        response.update(data)

    return jsonify(response), 200


def error_response(message="error", code=400):

    return jsonify({
        "status": "error",
        "message": message
    }), code
