from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "NUVIBANK API v2 online 🚀"

@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "system": "NUVIBANK",
        "version": "2.0"
    })

@app.route("/users")
def users():
    return jsonify({
        "users": []
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
