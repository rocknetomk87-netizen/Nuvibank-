from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nuvibank_v2_secure_key")

DB = os.environ.get("DB_NAME", "nuvibank.db")
CATEGORIES = ["Comida", "Transporte", "Casa", "Lazer", "Outros"]


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(conn, table_name, column_name):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = cur.fetchall()
    return any(col["name"] == column_name for col in cols)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT,
        created_at TEXT,
        ref TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    # Migrações simples para versões antigas
    if not column_exists(conn, "users", "goal"):
        cur.execute("ALTER TABLE users ADD COLUMN goal REAL DEFAULT 0")
        conn.commit()

    if not column_exists(conn, "transactions", "created_at"):
        cur.execute("ALTER TABLE transactions ADD COLUMN created_at TEXT")
        conn.commit()

    if not column_exists(conn, "transactions", "ref"):
        cur.execute("ALTER TABLE transactions ADD COLUMN ref TEXT")
        conn.commit()

    # Cria user inicial se não existir
    cur.execute("SELECT id FROM users WHERE username = ?", ("founder",))
    existing = cur.fetchone()

    if not existing:
        cur.execute("""
        INSERT INTO users (username, password, name, balance, goal)
        VALUES (?, ?, ?, ?, ?)
        """, ("founder", "1234", "Roque Ntchiendo", 1250000.0, 200000.0))
        conn.commit()
    else:
        # garante que founder tenha meta definida
        cur.execute("UPDATE users SET goal = COALESCE(goal, 200000) WHERE username = ?", ("founder",))
        conn.commit()

    conn.close()


def generate_ref():
    return f"NB-{random.randint(100000, 999999)}"


def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def create_user(name, username, password, balance=0.0):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO users (name, username, password, balance, goal)
    VALUES (?, ?, ?, ?, ?)
    """, (name, username, password, balance, 0.0))
    conn.commit()
    conn.close()


def get_transactions(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM transactions
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def add_transaction(user_id, amount, category, note):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO transactions (user_id, amount, category, note, created_at, ref)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        category,
        note,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        generate_ref()
    ))
    conn.commit()
    conn.close()


def update_user_balance(user_id, new_balance):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()


def update_user_goal(user_id, new_goal):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET goal = ? WHERE id = ?", (new_goal, user_id))
    conn.commit()
    conn.close()


def get_category_totals(transactions):
    totals = {category: 0.0 for category in CATEGORIES}
    for tx in transactions:
        category = tx["category"]
        amount = tx["amount"]
        if category in totals:
            totals[category] += amount
        else:
            totals["Outros"] += amount
    return totals


def get_total_spent(transactions):
    return sum(tx["amount"] for tx in transactions)


def get_alerts(category_totals, total_spent):
    alerts = []

    if total_spent <= 0:
        alerts.append("Sem dados suficientes para auditoria.")
        return alerts

    top_category = max(category_totals, key=category_totals.get)
    top_value = category_totals[top_category]
    top_percent = (top_value / total_spent) * 100 if total_spent > 0 else 0

    alerts.append(f"Maior categoria de gasto: {top_category} ({top_percent:.0f}%).")

    if top_percent >= 50:
        alerts.append(f"Atenção: mais de 50% dos gastos foram em {top_category}.")

    if total_spent > 200000:
        alerts.append("Atenção: gastos elevados neste período.")

    return alerts


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUVIBANK Lite v2</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1220;
            color: #ffffff;
        }
        .wrap {
            max-width: 760px;
            margin: 0 auto;
            padding: 16px;
        }
        .card {
            background: #111a2b;
            border: 1px solid #22304a;
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 16px;
        }
        h1, h2, h3 {
            margin-top: 0;
        }
        .brand {
            font-weight: bold;
            font-size: 24px;
            color: #7fb3ff;
        }
        .muted {
            color: #b3bfd1;
            font-size: 14px;
        }
        .balance {
            font-size: 28px;
            font-weight: bold;
            margin: 10px 0;
        }
        input, select, button {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin-top: 10px;
            border-radius: 10px;
            border: none;
            font-size: 15px;
        }
        button {
            background: #2f80ed;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .error {
            background: #4a1f28;
            color: #ffb3b3;
            padding: 10px;
            border-radius: 10px;
            margin-top: 12px;
        }
        .success {
            background: #15351f;
            color: #b8f5c8;
            padding: 10px;
            border-radius: 10px;
            margin-top: 12px;
        }
        ul {
            padding-left: 18px;
        }
        .top-line {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }
        .small {
            font-size: 13px;
            color: #b3bfd1;
        }
        .logout {
            color: #ffb0b0;
            text-decoration: none;
        }
        .metric {
            font-size: 16px;
            font-weight: bold;
        }
        .row {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        @media (min-width: 700px) {
            .row {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="wrap">
        {% if page == 'login' %}
            <div class="card">
                <div class="brand">NUVIBANK Lite v2</div>
                <p class="muted">Controlo financeiro pessoal com contas separadas por utilizador.</p>
                <h2>Entrar</h2>
                <form method="post" action="/login">
                    <input name="username" placeholder="Utilizador" required>
                    <input name="password" type="password" placeholder="Senha" required>
                    <button type="submit">Entrar</button>
                </form>
                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
            </div>

            <div class="card">
                <h3>Criar conta</h3>
                <form method="post" action="/register">
                    <input name="name" placeholder="Nome completo" required>
                    <input name="username" placeholder="Novo utilizador" required>
                    <input name="password" type="password" placeholder="Nova senha" required>
                    <input name="balance" placeholder="Saldo inicial (opcional)">
                    <button type="submit">Criar conta</button>
                </form>
                {% if register_error %}
                    <div class="error">{{ register_error }}</div>
                {% endif %}
                {% if register_message %}
                    <div class="success">{{ register_message }}</div>
                {% endif %}
            </div>

        {% elif page == 'dashboard' %}
            <div class="card">
                <div class="top-line">
                    <div>
                        <div class="brand">NUVIBANK Lite v2</div>
                        <div class="muted">Sistema simples de controlo financeiro pessoal</div>
                    </div>
                    <div class="small">
                        {{ name }}<br>
                        <a class="logout" href="/logout">Terminar sessão</a>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="card">
                    <h3>Saldo Atual</h3>
                    <div class="balance">{{ balance }} Kz</div>
                    <div class="small">Utilizador: {{ username }}</div>
                </div>

                <div class="card">
                    <h3>Meta Financeira</h3>
                    <div class="metric">Meta: {{ goal }} Kz</div>
                    <div class="metric">Gasto: {{ total_spent }} Kz</div>
                    <div class="small">Progresso: {{ progress_percent }}%</div>
                </div>
            </div>

            <div class="card">
                <h3>Registar Gasto</h3>
                <form method="post" action="/add">
                    <input name="amount" placeholder="Valor em Kz" required>
                    <select name="category" required>
                        {% for category in categories %}
                            <option value="{{ category }}">{{ category }}</option>
                        {% endfor %}
                    </select>
                    <input name="note" placeholder="Nota opcional">
                    <button type="submit">Adicionar Gasto</button>
                </form>

                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
                {% if message %}
                    <div class="success">{{ message }}</div>
                {% endif %}
            </div>

            <div class="card">
                <h3>Definir Meta</h3>
                <form method="post" action="/goal">
                    <input name="goal" placeholder="Meta mensal em Kz" required>
                    <button type="submit">Guardar Meta</button>
                </form>
            </div>

            <div class="card">
                <h3>Resumo por Categoria</h3>
                <ul>
                    {% for category, value in category_totals.items() %}
                        <li>{{ category }}: {{ value }} Kz</li>
                    {% endfor %}
                </ul>
            </div>

            <div class="card">
                <h3>Alertas</h3>
                <ul>
                    {% for alert in alerts %}
                        <li>{{ alert }}</li>
                    {% endfor %}
                </ul>
            </div>

            <div class="card">
                <h3>Histórico</h3>
                {% if transactions %}
                    <ul>
                        {% for tx in transactions %}
                            <li>
                                {{ tx["created_at"] }} |
                                {{ tx["category"] }} |
                                {{ tx["amount"] }} Kz |
                                {{ tx["ref"] }}
                                {% if tx["note"] %}
                                    | {{ tx["note"] }}
                                {% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="muted">Nenhum gasto registado ainda.</p>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


def render_login(error=None, register_error=None, register_message=None):
    return render_template_string(
        PAGE_TEMPLATE,
        page="login",
        error=error,
        register_error=register_error,
        register_message=register_message
    )


def render_dashboard(user_row, error=None, message=None):
    user_id = user_row["id"]
    transactions = get_transactions(user_id)
    category_totals = get_category_totals(transactions)
    total_spent = get_total_spent(transactions)
    alerts = get_alerts(category_totals, total_spent)

    goal = user_row["goal"] if user_row["goal"] is not None else 0.0
    progress_percent = 0
    if goal > 0:
        progress_percent = min(int((total_spent / goal) * 100), 999)

    return render_template_string(
        PAGE_TEMPLATE,
        page="dashboard",
        error=error,
        message=message,
        name=user_row["name"],
        username=user_row["username"],
        balance=f"{user_row['balance']:,.2f}",
        goal=f"{goal:,.2f}",
        total_spent=f"{total_spent:,.2f}",
        progress_percent=progress_percent,
        category_totals={k: f"{v:,.2f}" for k, v in category_totals.items()},
        alerts=alerts,
        transactions=transactions,
        categories=CATEGORIES
    )


@app.route("/", methods=["GET"])
def index():
    if session.get("user_id"):
        return redirect("/dashboard")
    return render_login()


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user_row = get_user_by_username(username)

    if not user_row or user_row["password"] != password:
        return render_login(error="Credenciais inválidas.")

    session["user_id"] = user_row["id"]
    return redirect("/dashboard")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    balance_raw = request.form.get("balance", "").strip().replace(",", ".")

    if not name or not username or not password:
        return render_login(register_error="Preenche nome, utilizador e senha.")

    if get_user_by_username(username):
        return render_login(register_error="Este utilizador já existe.")

    balance = 0.0
    if balance_raw:
        try:
            balance = float(balance_raw)
        except ValueError:
            return render_login(register_error="Saldo inicial inválido.")

        if balance < 0:
            return render_login(register_error="O saldo inicial não pode ser negativo.")

    create_user(name, username, password, balance)
    return render_login(register_message="Conta criada com sucesso. Já podes entrar.")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    user_row = get_user_by_id(user_id)
    if not user_row:
        session.clear()
        return redirect("/")

    return render_dashboard(user_row)


@app.route("/add", methods=["POST"])
def add_expense():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    user_row = get_user_by_id(user_id)
    if not user_row:
        session.clear()
        return redirect("/")

    amount_raw = request.form.get("amount", "").strip().replace(",", ".")
    category = request.form.get("category", "").strip()
    note = request.form.get("note", "").strip()

    if not amount_raw:
        return render_dashboard(user_row, error="O valor é obrigatório.")

    try:
        amount = float(amount_raw)
    except ValueError:
        return render_dashboard(user_row, error="Valor inválido. Introduz apenas números.")

    if amount <= 0:
        return render_dashboard(user_row, error="O valor deve ser maior que zero.")

    if category not in CATEGORIES:
        return render_dashboard(user_row, error="Categoria inválida.")

    if amount > user_row["balance"]:
        return render_dashboard(user_row, error="Saldo insuficiente para registar este gasto.")

    new_balance = user_row["balance"] - amount
    update_user_balance(user_id, new_balance)
    add_transaction(user_id, amount, category, note)

    updated_user = get_user_by_id(user_id)
    return render_dashboard(updated_user, message="Gasto registado com sucesso.")


@app.route("/goal", methods=["POST"])
def goal():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")

    user_row = get_user_by_id(user_id)
    if not user_row:
        session.clear()
        return redirect("/")

    goal_raw = request.form.get("goal", "").strip().replace(",", ".")

    if not goal_raw:
        return render_dashboard(user_row, error="A meta é obrigatória.")

    try:
        new_goal = float(goal_raw)
    except ValueError:
        return render_dashboard(user_row, error="Meta inválida. Introduz apenas números.")

    if new_goal < 0:
        return render_dashboard(user_row, error="A meta não pode ser negativa.")

    update_user_goal(user_id, new_goal)
    updated_user = get_user_by_id(user_id)
    return render_dashboard(updated_user, message="Meta guardada com sucesso.")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")


# Inicializa também quando importado pelo gunicorn
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
