from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# APP
# =========================================

app = Flask(__name__)
CORS(app)

# =========================================
# CONFIG
# =========================================

JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "NUVIBANK_SECRET"
)

DB_NAME = "nuvibank.db"

# =========================================
# INIT DATABASE
# =========================================

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance INTEGER DEFAULT 0,
        role TEXT DEFAULT 'user'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================================
# VERIFY TOKEN
# =========================================

def verify_token():

    token = request.headers.get("Authorization")

    if not token:
        return None

    try:

        data = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )

        return data

    except:
        return None

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("index.html")

# =========================================
# REGISTER
# =========================================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:

        return jsonify({
            "success": False,
            "message": "Dados inválidos"
        })

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Usuário já existe"
        })

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""
    INSERT INTO users (
        username,
        password,
        balance,
        role
    )
    VALUES (?, ?, ?, ?)
    """, (
        username,
        hashed_password,
        0,
        "user"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Conta criada"
    })

# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:

        return jsonify({
            "success": False,
            "message": "Conta não encontrada"
        })

    # =====================================
    # VERIFY PASSWORD
    # =====================================

    if not bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):

        return jsonify({
            "success": False,
            "message": "Password incorreta"
        })

    # =====================================
    # JWT TOKEN
    # =====================================

    token = jwt.encode({

        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)

    },
    JWT_SECRET,
    algorithm="HS256")

    return jsonify({
        "success": True,
        "token": token,
        "username": user["username"],
        "role": user["role"],
        "balance": user["balance"]
    })

# =========================================
# ACCOUNT
# =========================================

@app.route("/account", methods=["GET"])
def account():

    token_data = verify_token()

    if not token_data:

        return jsonify({
            "success": False,
            "message": "Token inválido"
        })

    username = token_data["username"]

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "username": user["username"],
        "balance": user["balance"],
        "role": user["role"]
    })

# =========================================
# TRANSFER
# =========================================

@app.route("/transfer", methods=["POST"])
def transfer():

    token_data = verify_token()

    if not token_data:

        return jsonify({
            "success": False,
            "message": "Token inválido"
        })

    data = request.json

    receiver = data.get("receiver")
    amount = data.get("amount")

    if not receiver or not amount:

        return jsonify({
            "success": False,
            "message": "Dados inválidos"
        })

    amount = int(amount)

    sender = token_data["username"]

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # =====================================
    # GET SENDER
    # =====================================

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (sender,)
    )

    sender_user = cursor.fetchone()

    # =====================================
    # GET RECEIVER
    # =====================================

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (receiver,)
    )

    receiver_user = cursor.fetchone()

    if not receiver_user:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Destinatário não encontrado"
        })

    if sender_user["balance"] < amount:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Saldo insuficiente"
        })

    # =====================================
    # UPDATE BALANCES
    # =====================================

    new_sender_balance = sender_user["balance"] - amount
    new_receiver_balance = receiver_user["balance"] + amount

    cursor.execute("""
    UPDATE users
    SET balance=?
    WHERE username=?
    """, (
        new_sender_balance,
        sender
    ))

    cursor.execute("""
    UPDATE users
    SET balance=?
    WHERE username=?
    """, (
        new_receiver_balance,
        receiver
    ))

    # =====================================
    # SAVE TRANSACTION
    # =====================================

    cursor.execute("""
    INSERT INTO transactions (
        sender,
        receiver,
        amount,
        created_at
    )
    VALUES (?, ?, ?, ?)
    """, (
        sender,
        receiver,
        amount,
        str(datetime.datetime.utcnow())
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Transferência realizada"
    })

# =========================================
# HISTORY
# =========================================

@app.route("/history", methods=["GET"])
def history():

    token_data = verify_token()

    if not token_data:

        return jsonify({
            "success": False,
            "message": "Token inválido"
        })

    username = token_data["username"]

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM transactions
    WHERE sender=? OR receiver=?
    ORDER BY id DESC
    """, (
        username,
        username
    ))

    transactions = cursor.fetchall()

    conn.close()

    result = []

    for tx in transactions:

        result.append({
            "sender": tx["sender"],
            "receiver": tx["receiver"],
            "amount": tx["amount"],
            "created_at": tx["created_at"]
        })

    return jsonify({
        "success": True,
        "transactions": result
    })

# =========================================
# ADMIN USERS
# =========================================

@app.route("/admin/users", methods=["GET"])
def admin_users():

    token_data = verify_token()

    if not token_data:

        return jsonify({
            "success": False,
            "message": "Token inválido"
        })

    if token_data["role"] != "admin":

        return jsonify({
            "success": False,
            "message": "Acesso negado"
        })

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, balance, role
    FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    result = []

    total_bank = 0

    for user in users:

        total_bank += user["balance"]

        result.append({
            "username": user["username"],
            "balance": user["balance"],
            "role": user["role"]
        })

    return jsonify({
        "success": True,
        "bank_total": total_bank,
        "users": result
    })

# =========================================
# START SERVER
# =========================================

if __name__ == "__main__":

    init_db()

    print("NUVIBANK V10 STARTED")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
