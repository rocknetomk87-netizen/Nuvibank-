from flask import Blueprint, jsonify

transfer_api = Blueprint("transfer_api", __name__)

@transfer_api.route("/transfer", methods=["POST"])
def transfer():

    return jsonify({
        "status": "success",
        "message": "transfer_completed"
    }), 200
