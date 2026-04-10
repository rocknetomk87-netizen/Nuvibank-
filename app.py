from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nuvibank.db")
JWT_SECRET = os.environ.get("JWT_SECRET", "CHANGE_THIS_NUVIBANK_JWT_SECRET")
JWT_ALGORITHM = "HS256"
TOKEN_EXP_HOURS = 24

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUVIBANK v6.1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 820px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }
        h1, h2 {
            margin-top: 0;
        }
        input, button, textarea {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            margin-bottom: 10px;
            border-radius: 10px;
            border: none;
            box-sizing: border-box;
            font-size: 15px;
        }
        input, textarea {
            background: #e2e8f0;
            color: #111827;
        }
        button {
            background: #7c3aed;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            opacity: 0.94;
        }
        .secondary {
            background: #334155;
        }
        .danger {
            background: #b91c1c;
        }
        .result, .box {
            white-space: pre-wrap;
            background: #020617;
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
            overflow-x: auto;
        }
        .row {
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #334155;
        }
        .row:last-child {
            border-bottom: none;
        }
        .muted {
            color: #cbd5e1;
            font-size: 13px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>NUVIBANK v6.1</h1>
            <p class="muted">JWT, rotas protegidas e identidade real do utilizador.</p>
        </div>

        <div class="card">
            <h2>Conta</h2>
            <input type="text" id="register_name" placeholder="Nome do utilizador">
            <input type="password" id="register_password" placeholder="Password">
            <button onclick="registerUser()">Criar conta</button>
        </div>

        <div class="card">
            <h2>Login</h2>
            <input type="text" id="login_name" placeholder="Nome do utilizador">
            <input type="password" id="login_password" placeholder="Password">
            <button onclick="loginUser()">Entrar</button>
            <button class="danger" onclick="logoutUser()">Sair</button>
        </div>

        <div class="card">
            <h2>Sessão atual</h2>
            <button class="secondary" onclick="loadMe()">Atualizar sessão</button>
            <div id="me" class="box">Sem token.</div>
        </div>

        <div id="secure-zone" class="hidden">
            <div class="card">
                <h2>Depositar</h2>
                <input type="number" id="deposit_amount" placeholder="Valor do depósito">
                <button onclick="depositMoney()">Depositar na minha conta</button>
            </div>

            <div class="card">
                <h2>Transferir</h2>
                <input type="number" id="transfer_to" placeholder="ID destino">
                <input type="number" id="transfer_amount" placeholder="Valor da transferência">
                <button onclick="transferMoney()">Transferir</button>
            </div>

            <div class="card">
                <h2>Meu extrato</h2>
                <button class="secondary" onclick="loadMyTransactions()">Atualizar meu extrato</button>
                <div id="my-transactions" class="box">Sem dados.</div>
            </div>
        </div>

        <div class="card">
            <h2>Utilizadores</h2>
            <button class="secondary" onclick="loadUsers()">Atualizar utilizadores</button>
            <div id="users" class="box">Sem dados.</div>
        </div>

        <div class="card">
            <h2>Todas as transações</h2>
            <button class="secondary" onclick="loadTransactions()">Atualizar transações</button>
            <div id="transactions" class="box">Sem dados.</div>
        </div>

        <div class="card">
            <h2>Resultado</h2>
            <div id="result" class="result">Pronto.</div>
        </div>
    </div>

    <script>
        let authToken = localStorage.getItem("nuvibank_token") || "";

        function setResult(data) {
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
        }

        function getHeaders() {
            const headers = { "Content-Type": "application/json" };
            if (authToken) {
                headers["Authorization"] = "Bearer " + authToken;
            }
            return headers;
        }

        function setSecureZone(visible) {
            const zone = document.getElementById("secure-zone");
            if (visible) {
                zone.classList.remove("hidden");
            } else {
                zone.classList.add("hidden");
            }
        }

        async function registerUser() {
            const name = document.getElementById("register_name").value.trim();
            const password = document.getElementById("register_password").value;

            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, password })
            });

            const data = await response.json();
            setResult(data);
            loadUsers();
        }

        async function loginUser() {
            const name = document.getElementById("login_name").value.trim();
            const password = document.getElementById("login_password").value;

            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, password })
            });

            const data = await response.json();
            if (data.token) {
                authToken = data.token;
                localStorage.setItem("nuvibank_token", authToken);
            }
            setResult(data);
            await loadMe();
            await loadMyTransactions();
        }

        function logoutUser() {
            authToken = "";
            localStorage.removeItem("nuvibank_token");
            setSecureZone(false);
            document.getElementById("me").textContent = "Sem token.";
            document.getElementById("my-transactions").textContent = "Sem dados.";
            setResult({ message: "Logout local realizado com sucesso." });
        }

        async function loadMe() {
            if (!authToken) {
                setSecureZone(false);
                document.getElementById("me").textContent = "Sem token.";
                return;
            }

            const response = await fetch("/me", {
                method: "GET",
                headers: getHeaders()
            });

            const data = await response.json();

            if (response.ok && data.user) {
                setSecureZone(true);
                document.getElementById("me").innerHTML =
                    "<strong>ID:</strong> " + data.user.id + "<br>" +
                    "<strong>Nome:</strong> " + data.user.name + "<br>" +
                    "<strong>Saldo:</strong> " + data.user.balance;
            } else {
                setSecureZone(false);
                document.getElementById("me").textContent = "Token inválido ou expirado.";
                localStorage.removeItem("nuvibank_token");
                authToken = "";
            }
        }

        async function depositMoney() {
            const amount = Number(document.getElementById("deposit_amount").value);

            const response = await fetch("/deposit", {
                method: "POST",
                headers: getHeaders(),
                body: JSON.stringify({ amount })
            });

            const data = await response.json();
            setResult(data);
            await loadMe();
            await loadUsers();
            await loadTransactions();
            await loadMyTransactions();
        }

        async function transferMoney() {
            const to_user_id = Number(document.getElementById("transfer_to").value);
            const amount = Number(document.getElementById("transfer_amount").value);

            const response = await fetch("/transfer", {
                method: "POST",
                headers: getHeaders(),
                body: JSON.stringify({ to_user_id, amount })
            });

            const data = await response.json();
            setResult(data);
            await loadMe();
            await loadUsers();
            await loadTransactions();
            await loadMyTransactions();
        }

        async function loadUsers() {
            const response = await fetch("/users");
            const data = await response.json();

            if (!data.users || data.users.length === 0) {
                document.getElementById("users").textContent = "Nenhum utilizador criado.";
                return;
            }

            const html = data.users.map(user => `
                <div class="row">
                    <strong>ID:</strong> ${user.id}<br>
                    <strong>Nome:</strong> ${user.name}<br>
                    <strong>Saldo:</strong> ${user.balance}
                </div>
            `).join("");

            document.getElementById("users").innerHTML = html;
        }

        async function loadTransactions() {
            const response = await fetch("/transactions");
            const data = await response.json();

            if (!data.transactions || data.transactions.length === 0) {
                document.getElementById("transactions").textContent = "Nenhuma transação registada.";
                return;
            }

            const html = data.transactions.map(tx => `
                <div class="row">
                    <strong>ID:</strong> ${tx.id}<br>
                    <strong>Tipo:</strong> ${tx.type}<br>
                    <strong>Valor:</strong> ${tx.amount}<br>
                    <strong>Origem:</strong> ${tx.from_user_id ?? "-"}<br>
                    <strong>Destino:</strong> ${tx.to_user_id ?? "-"}<br>
                    <strong>Data:</strong> ${tx.created_at}
                </div>
            `).join("");

            document.getElementById("transactions").innerHTML = html;
        }

        async function loadMyTransactions() {
            if (!authToken) {
                document.getElementById("my-transactions").textContent = "Sem token.";
                return;
            }

            const response = await fetch("/my-transactions", {
                method: "GET",
                headers: getHeaders()
            });

            const data = await response.json();

            if (!response.ok) {
                document.getElementById("my-transactions").textContent = data.error || "Erro ao carregar extrato.";
                return;
            }

            if (!data.transactions || data.transactions.length === 0) {
                document.getElementById("my-transactions").textContent = "Nenhuma transação tua ainda.";
                return;
            }

            const html = data.transactions.map(tx => `
                <div class="row">
                    <strong>ID:</strong> ${tx.id}<br>
                    <strong>Tipo:</strong> ${tx.type}<br>
                    <strong>Valor:</strong> ${tx.amount}<br>
                    <strong>Origem:</strong> ${tx.from_user_id ?? "-"}<br>
                    <strong>Destino:</strong> ${tx.to_user_id ?? "-"}<br>
                    <strong>Data:</strong> ${tx.created_at}
                </div>
            `).join("");

            document.getElementById("my-transactions").innerHTML = html;
        }

        loadMe();
        loadUsers();
        loadTransactions();
        loadMyTransactions();
    </script>
</body>
</html>
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return dict(row) if row is not None else None


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password_hash TEXT,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    cur.execute("PRAGMA table_info(users)")
    columns = [row["name"] for row in cur.fetchall()]

    if "password_hash" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            from_user_id INTEGER,
            to_user_id INTEGER,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_token(user_id: int, name: str):
    payload = {
        "user_id": user_id,
        "name": name,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXP_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def auth_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token obrigatório."}), 401

        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 401

        request.current_user = {
            "id": payload["user_id"],
            "name": payload["name"]
        }
        return route_function(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "v6.1"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    password = str(data.get("password", "")).strip()

    if not name:
        return jsonify({"error": "O campo 'name' é obrigatório."}), 400

    if len(name) < 2:
        return jsonify({"error": "O nome deve ter pelo menos 2 caracteres."}), 400

    if not password:
        return jsonify({"error": "O campo 'password' é obrigatório."}), 400

    if len(password) < 4:
        return jsonify({"error": "A password deve ter pelo menos 4 caracteres."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE LOWER(name) = LOWER(?)", (name,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return jsonify({"error": "Já existe um utilizador com esse nome."}), 409

    password_hash = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (name, password_hash, balance) VALUES (?, ?, ?)",
        (name, password_hash, 0.0)
    )
    user_id = cur.lastrowid
    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    user = row_to_dict(cur.fetchone())
    conn.close()

    return jsonify({
        "message": "Conta criada com sucesso.",
        "user": user
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    password = str(data.get("password", "")).strip()

    if not name or not password:
        return jsonify({"error": "Nome e password são obrigatórios."}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, password_hash, balance FROM users WHERE LOWER(name) = LOWER(?)",
        (name,)
    )
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Utilizador não encontrado."}), 404

    if not user["password_hash"] or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Password inválida."}), 401

    token = generate_token(user["id"], user["name"])

    return jsonify({
        "message": "Login realizado com sucesso.",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "balance": user["balance"]
        }
    })


@app.route("/me", methods=["GET"])
@auth_required
def me():
    current = request.current_user

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current["id"],))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Utilizador não encontrado."}), 404

    return jsonify({"user": row_to_dict(user)})


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM users ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    users = [row_to_dict(row) for row in rows]

    return jsonify({
        "total": len(users),
        "users": users
    })


@app.route("/deposit", methods=["POST"])
@auth_required
def deposit():
    data = request.get_json(silent=True) or {}
    current = request.current_user

    if "amount" not in data:
        return jsonify({"error": "O campo 'amount' é obrigatório."}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Valor inválido."}), 400

    if amount <= 0:
        return jsonify({"error": "O valor deve ser maior que zero."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current["id"],))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "Utilizador não encontrado."}), 404

    new_balance = float(user["balance"]) + amount

    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, current["id"]))
    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("deposit", None, current["id"], amount, datetime.now(timezone.utc).isoformat()))

    conn.commit()
    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current["id"],))
    updated_user = row_to_dict(cur.fetchone())
    conn.close()

    return jsonify({
        "message": "Depósito realizado com sucesso.",
        "user": updated_user
    })


@app.route("/transfer", methods=["POST"])
@auth_required
def transfer():
    data = request.get_json(silent=True) or {}
    current = request.current_user

    if "to_user_id" not in data or "amount" not in data:
        return jsonify({"error": "Os campos 'to_user_id' e 'amount' são obrigatórios."}), 400

    try:
        to_user_id = int(data["to_user_id"])
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Dados inválidos."}), 400

    if amount <= 0:
        return jsonify({"error": "O valor da transferência deve ser maior que zero."}), 400

    if current["id"] == to_user_id:
        return jsonify({"error": "Não pode transferir para a mesma conta."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current["id"],))
    sender = cur.fetchone()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (to_user_id,))
    receiver = cur.fetchone()

    if sender is None:
        conn.close()
        return jsonify({"error": "Conta de origem não encontrada."}), 404

    if receiver is None:
        conn.close()
        return jsonify({"error": "Conta de destino não encontrada."}), 404

    sender_balance = float(sender["balance"])
    receiver_balance = float(receiver["balance"])

    if sender_balance < amount:
        conn.close()
        return jsonify({"error": "Saldo insuficiente."}), 400

    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (sender_balance - amount, current["id"]))
    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (receiver_balance + amount, to_user_id))
    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("transfer", current["id"], to_user_id, amount, datetime.now(timezone.utc).isoformat()))

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current["id"],))
    updated_sender = row_to_dict(cur.fetchone())

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (to_user_id,))
    updated_receiver = row_to_dict(cur.fetchone())

    conn.close()

    return jsonify({
        "message": "Transferência realizada com sucesso.",
        "from_user": updated_sender,
        "to_user": updated_receiver,
        "amount": amount
    })


@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, type, from_user_id, to_user_id, amount, created_at
        FROM transactions
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    transactions = [row_to_dict(row) for row in rows]

    return jsonify({
        "total": len(transactions),
        "transactions": transactions
    })


@app.route("/my-transactions", methods=["GET"])
@auth_required
def my_transactions():
    current = request.current_user

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, type, from_user_id, to_user_id, amount, created_at
        FROM transactions
        WHERE from_user_id = ? OR to_user_id = ?
        ORDER BY id DESC
    """, (current["id"], current["id"]))
    rows = cur.fetchall()
    conn.close()

    transactions = [row_to_dict(row) for row in rows]

    return jsonify({
        "total": len(transactions),
        "transactions": transactions
    })


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
