from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "app": "NUVIBANK",
        "status": "online 🚀",
        "version": "v2"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "ok"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "message": "API NUVIBANK funcionando 💰"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
