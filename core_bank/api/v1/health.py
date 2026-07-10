from flask import Blueprint, jsonify
from datetime import datetime

health = Blueprint("health", __name__)

@health.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "service": "NUVIBANK CORE",
        "timestamp": datetime.utcnow().isoformat()
    }), 200
