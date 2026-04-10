from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nuvibank.db")


HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUVIBANK v5</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 760px;
            margin: 0 auto;
        }
        .card {
            background: #1e293b;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        }
        h1, h2 {
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
        .result {
            white-space: pre-wrap;
            background: #020617;
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
            overflow-x: auto;
        }
        .user-list, .tx-list {
            background: #020617;
            border-radius: 10px;
            padding: 12px;
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
        .grid {
            display: grid;
            gap: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>NUVIBANK v5</h1>
            <p class="small">Sistema com SQLite e persistência real.</p>
        </div>

        <div class="card">
            <h2>Criar utilizador</h2>
            <input type="text" id="create_name" placeholder="Nome do utilizador">
            <button onclick="createUser()">Criar utilizador</button>
        </div>

        <div class="card">
            <h2>Depositar saldo</h2>
            <input type="number" id="deposit_user_id" placeholder="ID do utilizador">
            <input type="number" id="deposit_amount" placeholder="Valor do depósito">
            <button onclick="depositMoney()">Depositar</button>
        </div>

        <div class="card">
            <h2>Transferir</h2>
            <input type="number" id="from_user_id" placeholder="ID remetente">
            <input type="number" id="to_user_id" placeholder="ID destinatário">
            <input type="number" id="transfer_amount" placeholder="Valor da transferência">
            <button onclick="transferMoney()">Transferir</button>
        </div>

        <div class="card">
            <h2>Utilizadores</h2>
            <button class="secondary" onclick="loadUsers()">Atualizar utilizadores</button>
            <div id="users" class="user-list">Sem dados ainda.</div>
        </div>

        <div class="card">
            <h2>Transações</h2>
            <button class="secondary" onclick="loadTransactions()">Atualizar transações</button>
            <div id="transactions" class="tx-list">Sem transações ainda.</div>
        </div>

        <div class="card">
            <h2>Resultado</h2>
            <div id="result" class="result">Pronto.</div>
        </div>
    </div>

    <script>
        async function createUser() {
            const name = document.getElementById("create_name").value.trim();

            const response = await fetch("/users", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ name })
            });

            const data = await response.json();
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
            loadUsers();
        }

        async function depositMoney() {
            const user_id = Number(document.getElementById("deposit_user_id").value);
            const amount = Number(document.getElementById("deposit_amount").value);

            const response = await fetch("/deposit", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_id, amount })
            });

            const data = await response.json();
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
            loadUsers();
            loadTransactions();
        }

        async function transferMoney() {
            const from_user_id = Number(document.getElementById("from_user_id").value);
            const to_user_id = Number(document.getElementById("to_user_id").value);
            const amount = Number(document.getElementById("transfer_amount").value);

            const response = await fetch("/transfer", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ from_user_id, to_user_id, amount })
            });

            const data = await response.json();
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
            loadUsers();
            loadTransactions();
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

        loadUsers();
        loadTransactions();
    </script>
</body>
</html>
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

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


def row_to_dict(row):
    return dict(row) if row is not None else None


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db": "sqlite"})


@app.route("/api/test", methods=["GET"])
def api_test():
    return jsonify({"message": "API NUVIBANK v5 funcionando"})


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


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({"error": "O campo 'name' é obrigatório."}), 400

    if len(name) < 2:
        return jsonify({"error": "O nome deve ter pelo menos 2 caracteres."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE LOWER(name) = LOWER(?)", (name,))
    exists = cur.fetchone()
    if exists:
        conn.close()
        return jsonify({"error": "Já existe um utilizador com esse nome."}), 409

    cur.execute(
        "INSERT INTO users (name, balance) VALUES (?, ?)",
        (name, 0.0)
    )
    user_id = cur.lastrowid

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    user = row_to_dict(cur.fetchone())

    conn.close()

    return jsonify({
        "message": "Utilizador criado com sucesso.",
        "user": user
    }), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Utilizador não encontrado."}), 404

    return jsonify(row_to_dict(user))


@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json(silent=True) or {}

    if "user_id" not in data or "amount" not in data:
        return jsonify({
            "error": "Os campos 'user_id' e 'amount' são obrigatórios."
        }), 400

    try:
        user_id = int(data["user_id"])
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Os valores de 'user_id' ou 'amount' são inválidos."
        }), 400

    if amount <= 0:
        return jsonify({"error": "O valor deve ser maior que zero."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "Utilizador não encontrado."}), 404

    new_balance = float(user["balance"]) + amount

    cur.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_balance, user_id)
    )

    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("deposit", None, user_id, amount, datetime.utcnow().isoformat()))

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    updated_user = row_to_dict(cur.fetchone())

    conn.close()

    return jsonify({
        "message": "Depósito realizado com sucesso.",
        "user": updated_user
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json(silent=True) or {}

    required_fields = ["from_user_id", "to_user_id", "amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"O campo '{field}' é obrigatório."}), 400

    try:
        from_user_id = int(data["from_user_id"])
        to_user_id = int(data["to_user_id"])
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Os dados enviados são inválidos."}), 400

    if amount <= 0:
        return jsonify({"error": "O valor da transferência deve ser maior que zero."}), 400

    if from_user_id == to_user_id:
        return jsonify({"error": "Não pode transferir para a mesma conta."}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (from_user_id,))
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
        (new_sender_balance, from_user_id)
    )
    cur.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_receiver_balance, to_user_id)
    )

    cur.execute("""
        INSERT INTO transactions (type, from_user_id, to_user_id, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("transfer", from_user_id, to_user_id, amount, datetime.utcnow().isoformat()))

    conn.commit()

    cur.execute("SELECT id, name, balance FROM users WHERE id = ?", (from_user_id,))
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


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
