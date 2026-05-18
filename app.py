from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import jwt
from datetime import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = "NUVIBANK_ULTRA_SECRET"

DATABASE = "nuvibank.db"


# =========================
# DATABASE
# =========================

def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance INTEGER DEFAULT 500000
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Preencha todos campos"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()

        return jsonify({
            "error": "Utilizador já existe"
        }), 400

    cursor.execute("""
    INSERT INTO users(username, password)
    VALUES (?, ?)
    """, (username, password))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Conta criada"
    })


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({
            "error": "Login inválido"
        }), 401

    token = jwt.encode({
        "username": username
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token
    })


# =========================
# BALANCE
# =========================

@app.route("/balance", methods=["GET"])
def balance():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({
            "error": "Token missing"
        }), 401

    try:

        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = data["username"]

    except:
        return jsonify({
            "error": "Invalid token"
        }), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT balance FROM users
    WHERE username=?
    """, (username,))

    result = cursor.fetchone()

    conn.close()

    if not result:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "username": username,
        "balance": result[0]
    })


# =========================
# TRANSFER
# =========================

@app.route("/transfer", methods=["POST"])
def transfer():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({
            "error": "Token missing"
        }), 401

    try:

        data_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = data_token["username"]

    except:
        return jsonify({
            "error": "Invalid token"
        }), 401

    data = request.json

    receiver = data.get("receiver")
    amount = int(data.get("amount"))

    if amount <= 0:
        return jsonify({
            "error": "Valor inválido"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # remetente
    cursor.execute("""
    SELECT balance FROM users
    WHERE username=?
    """, (username,))

    sender_data = cursor.fetchone()

    if not sender_data:
        conn.close()

        return jsonify({
            "error": "Utilizador não encontrado"
        }), 404

    sender_balance = sender_data[0]

    if sender_balance < amount:
        conn.close()

        return jsonify({
            "error": "Saldo insuficiente"
        }), 400

    # destinatário
    cursor.execute("""
    SELECT * FROM users
    WHERE username=?
    """, (receiver,))

    receiver_data = cursor.fetchone()

    if not receiver_data:
        conn.close()

        return jsonify({
            "error": "Destinatário não existe"
        }), 404

    # atualizar remetente
    cursor.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE username=?
    """, (amount, username))

    # atualizar destinatário
    cursor.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE username=?
    """, (amount, receiver))

    # histórico
    cursor.execute("""
    INSERT INTO history(
        sender,
        receiver,
        amount,
        created_at
    )
    VALUES (?, ?, ?, ?)
    """, (
        username,
        receiver,
        amount,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Transferência realizada"
    })


# =========================
# HISTORY
# =========================

@app.route("/history", methods=["GET"])
def history():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({
            "error": "Token missing"
        }), 401

    try:

        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = data["username"]

    except:
        return jsonify({
            "error": "Invalid token"
        }), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT sender, receiver, amount, created_at
    FROM history
    WHERE sender=? OR receiver=?
    ORDER BY id DESC
    """, (username, username))

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({
            "sender": row[0],
            "receiver": row[1],
            "amount": row[2],
            "date": row[3]
        })

    return jsonify(history)


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
