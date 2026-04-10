from flask import Flask, request, jsonify, session, render_template_string
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"

DB = "nuvibank.db"

# ================= DB =================
def get_db():
    return sqlite3.connect(DB)

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        from_user INTEGER,
        to_user INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= AUTH =================

def auth_required():
    if "user_id" not in session:
        return False
    return True

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string("""
    <h2>NUVIBANK V6 🔐</h2>

    <h3>Login</h3>
    <input id="login_name" placeholder="Nome"><br>
    <input id="login_pass" type="password" placeholder="Password"><br>
    <button onclick="login()">Login</button>

    <h3>Criar conta</h3>
    <input id="name" placeholder="Nome"><br>
    <input id="pass" type="password" placeholder="Password"><br>
    <button onclick="createUser()">Criar</button>

    <h3>Depositar</h3>
    <input id="amount" placeholder="Valor"><br>
    <button onclick="deposit()">Depositar</button>

    <h3>Transferir</h3>
    <input id="to" placeholder="ID destino"><br>
    <input id="amount2" placeholder="Valor"><br>
    <button onclick="transfer()">Transferir</button>

    <pre id="result"></pre>

    <script>
    function show(r){document.getElementById("result").innerText=JSON.stringify(r,null,2)}

    function createUser(){
        fetch('/create_user',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            name:document.getElementById("name").value,
            password:document.getElementById("pass").value
        })}).then(r=>r.json()).then(show)
    }

    function login(){
        fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            name:document.getElementById("login_name").value,
            password:document.getElementById("login_pass").value
        })}).then(r=>r.json()).then(show)
    }

    function deposit(){
        fetch('/deposit',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            amount:document.getElementById("amount").value
        })}).then(r=>r.json()).then(show)
    }

    function transfer(){
        fetch('/transfer',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            to:document.getElementById("to").value,
            amount:document.getElementById("amount2").value
        })}).then(r=>r.json()).then(show)
    }
    </script>
    """)

# ================= USER =================

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    name = data["name"]
    password = generate_password_hash(data["password"])

    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
    conn.commit()

    user_id = c.lastrowid
    conn.close()

    return jsonify({"message": "Conta criada", "id": user_id})

# ================= LOGIN =================

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data["name"]
    password = data["password"]

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id, password FROM users WHERE name=?", (name,))
    user = c.fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):
        session["user_id"] = user[0]
        return jsonify({"message": "Login OK"})
    
    return jsonify({"error": "Credenciais inválidas"}), 401

# ================= DEPOSIT =================

@app.route("/deposit", methods=["POST"])
def deposit():
    if not auth_required():
        return jsonify({"error": "Login necessário"}), 403

    data = request.json
    amount = float(data["amount"])
    user_id = session["user_id"]

    conn = get_db()
    c = conn.cursor()

    c.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))

    c.execute("""
    INSERT INTO transactions (type, amount, from_user, to_user, date)
    VALUES (?, ?, ?, ?, ?)
    """, ("deposit", amount, None, user_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"message": "Depósito OK"})

# ================= TRANSFER =================

@app.route("/transfer", methods=["POST"])
def transfer():
    if not auth_required():
        return jsonify({"error": "Login necessário"}), 403

    data = request.json
    to_id = int(data["to"])
    amount = float(data["amount"])
    from_id = session["user_id"]

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE id=?", (from_id,))
    balance = c.fetchone()[0]

    if balance < amount:
        return jsonify({"error": "Saldo insuficiente"}), 400

    c.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, from_id))
    c.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, to_id))

    c.execute("""
    INSERT INTO transactions (type, amount, from_user, to_user, date)
    VALUES (?, ?, ?, ?, ?)
    """, ("transfer", amount, from_id, to_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"message": "Transferência OK"})

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
