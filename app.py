from flask import Flask, request, jsonify, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nuvibank.db")

# IMPORTANTE:
# No Render, cria a variável SECRET_KEY.
# Se não existir, usa esta temporária.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "CHANGE_ME_NUVIBANK_V6_1"
)

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
            max-width: 780px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        }
        h1, h2, h3 {
            margin-top: 0;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            margin-bottom: 10px;
            border-radius: 10px;
            border: none;
            box-sizing: border-box;
            font-size: 15px;
        }
        input {
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
            opacity: 0.92;
        }
        .secondary {
            background: #334155;
        }
        .danger {
            background: #b91c1c;
        }
        .result, .session-box, .user-list, .tx-list {
            white-space: pre-wrap;
            background: #020617;
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
            overflow-x: auto;
        }
        .small {
            color: #cbd5e1;
            font-size: 13px;
        }
        .row {
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #334155;
        }
        .row:last-child {
            border-bottom: none;
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
            <p class="small">Blindagem inicial, sessão, extrato e UX melhor.</p>
        </div>

        <div class="card">
            <h2>Sessão atual</h2>
            <button class="secondary" onclick="loadMe()">Atualizar sessão</button>
            <div id="me" class="session-box">Sem sessão iniciada.</div>
            <button class="danger" onclick="logoutUser()">Sair</button>
        </div>

        <div class="card">
            <h2>Criar conta</h2>
            <input type="text" id="register_name" placeholder="Nome do utilizador">
            <input type="password" id="register_password" placeholder="Password">
            <button onclick="registerUser()">Criar conta</button>
        </div>

        <div class="card">
            <h2>Entrar</h2>
            <input type="text" id="login_name" placeholder="Nome do utilizador">
            <input type="password" id="login_password" placeholder="Password">
            <button onclick="loginUser()">Entrar</button>
        </div>

        <div id="secure-actions" class="hidden">
            <div class="card">
                <h2>Depositar saldo</h2>
                <input type="number" id="deposit_amount" placeholder="Valor do depósito">
                <button onclick="depositMoney()">Depositar na minha conta</button>
            </div>

            <div class="card">
                <h2>Transferir</h2>
                <input type="number" id="to_user_id" placeholder="ID destinatário">
                <input type="number" id="transfer_amount" placeholder="Valor da transferência">
                <button onclick="transferMoney()">Transferir da minha conta</button>
            </div>

            <div class="card">
                <h2>Meu extrato</h2>
                <button class="secondary" onclick="loadMyTransactions()">Atualizar meu extrato</button>
                <div id="my-transactions" class="tx-list">Sem sessão iniciada.</div>
            </div>
        </div>

        <div class="card">
            <h2>Utilizadores</h2>
            <button class="secondary" onclick="loadUsers()">Atualizar utilizadores</button>
            <div id="users" class="user-list">Sem dados ainda.</div>
        </div>

        <div class="card">
            <h2>Todas as transações</h2>
            <button class="secondary" onclick="loadTransactions()">Atualizar transações</button>
            <div id="transactions" class="tx-list">Sem transações ainda.</div>
        </div>

        <div class="card">
            <h2>Resultado</h2>
            <div id="result" class="result">Pronto.</div>
        </div>
    </div>

    <script>
        function setResult(data) {
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
        }

        function setSecureVisible(isVisible) {
            const box = document.getElementById("secure-actions");
            if (isVisible) {
                box.classList.remove("hidden");
            } else {
                box.classList.add("hidden");
            }
        }

        async function registerUser() {
            const name = document.getElementById("register_name").value.trim();
            const password = document.getElementById("register_password").value;

            const response = await fetch("/register", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
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
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ name, password })
            });

            const data = await response.json();
            setResult(data);
            await loadMe();
            await loadUsers();
            await loadTransactions();
            await loadMyTransactions();
        }

        async function logoutUser() {
            const response = await fetch("/logout", {
                method: "POST"
            });

            const data = await response.json();
            setResult(data);
            await loadMe();
            document.getElementById("my-transactions").textContent = "Sem sessão iniciada.";
        }

        async function loadMe() {
            const response = await fetch("/me");
            const data = await response.json();

            if (data.authenticated) {
                document.getElementById("me").innerHTML = `
                    <strong>ID:</strong> ${data.user.id}<br>
                    <strong>Nome:</strong> ${data.user.name}<br>
                    <strong>Saldo:</strong> ${data.user.balance}
                `;
                setSecureVisible(true);
            } else {
                document.getElementById("me").textContent = "Sem sessão iniciada.";
                setSecureVisible(false);
            }
        }

        async function depositMoney() {
            const amount = Number(document.getElementById("deposit_amount").value);

            const response = await fetch("/deposit", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
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
            const to_user_id = Number(document.getElementById("to_user_id").value);
            const amount = Number(document.getElementById("transfer_amount").value);

            const response = await fetch("/transfer", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
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
            const response = await fetch("/my-transactions");
            const data = await response.json();

            if (data.error) {
                document.getElementById("my-transactions").textContent = data.error;
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
            password_hash TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    cur.execute("PRAGMA table_info(users)")
    columns = [row["name"] for row in cur.fetchall()]
    if "password_hash" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        default_hash = generate_password_hash("123456")
        cur.execute(
            "UPDATE users SET password_hash = ? WHERE password_hash IS NULL OR password_hash = ''",
            (default_hash,)
        )

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


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()

    return row_to_dict(user)


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": "v6.1"})


@app.route("/api/test", methods=["GET"])
def api_test():
    return jsonify({"message": "API NUVIBANK v6.1 funcionando"})


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
    exists = cur.fetchone()
    if exists:
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

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Login realizado com sucesso.",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "balance": user["balance"]
        }
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Sessão terminada com sucesso."})


@app.route("/me", methods=["GET"])
def me():
    user = get_current_user()
    if user is None:
        return jsonify({
            "authenticated": False,
            "user": None
        })

    return jsonify({
        "authenticated": True,
        "user": user
    })


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
def deposit():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "É necessário iniciar sessão."}), 401

    data = request.get_json(silent=True) or {}

    if "amount" not in data:
        return jsonify({"error": "O campo 'amount' é obrigatório."}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "O valor enviado é inválido."}), 400

    if amount <= 0:
        return jsonify({"error": "O valor deve ser maior que zero."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current_user["id"],))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "Utilizador não encontrado."}), 404

    new_balance = float(user["balance"]) + amount

    cur.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_balance, current_user["id"])
    )

    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("deposit", None, current_user["id"], amount, datetime.utcnow().isoformat()))

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current_user["id"],))
    updated_user = row_to_dict(cur.fetchone())
    conn.close()

    return jsonify({
        "message": "Depósito realizado com sucesso.",
        "user": updated_user
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "É necessário iniciar sessão."}), 401

    data = request.get_json(silent=True) or {}

    if "to_user_id" not in data or "amount" not in data:
        return jsonify({"error": "Os campos 'to_user_id' e 'amount' são obrigatórios."}), 400

    try:
        to_user_id = int(data["to_user_id"])
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Os dados enviados são inválidos."}), 400

    if amount <= 0:
        return jsonify({"error": "O valor da transferência deve ser maior que zero."}), 400

    if current_user["id"] == to_user_id:
        return jsonify({"error": "Não pode transferir para a mesma conta."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current_user["id"],))
    sender = cur.fetchone()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (to_user_id,))
    receiver = cur.fetchone()

    if sender is None:
        conn.close()
        return jsonify({"error": "Utilizador remetente não encontrado."}), 404

    if receiver is None:
        conn.close()
        return jsonify({"error": "Utilizador destinatário não encontrado."}), 404

    sender_balance = float(sender["balance"])
    receiver_balance = float(receiver["balance"])

    if sender_balance < amount:
        conn.close()
        return jsonify({"error": "Saldo insuficiente."}), 400

    new_sender_balance = sender_balance - amount
    new_receiver_balance = receiver_balance + amount

    cur.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_sender_balance, current_user["id"])
    )
    cur.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_receiver_balance, to_user_id)
    )

    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("transfer", current_user["id"], to_user_id, amount, datetime.utcnow().isoformat()))

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (current_user["id"],))
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
def my_transactions():
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"error": "É necessário iniciar sessão."}), 401

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, type, from_user_id, to_user_id, amount, created_at
        FROM transactions
        WHERE from_user_id = ? OR to_user_id = ?
        ORDER BY id DESC
    """, (current_user["id"], current_user["id"]))
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
