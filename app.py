from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from datetime import datetime
import os
import random
import calendar

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nuvibank_level2_secret")

DB = os.environ.get("DB_NAME", "nuvibank.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

EXPENSE_CATEGORIES = ["Comida", "Transporte", "Casa", "Lazer", "Outros"]
INCOME_CATEGORIES = ["Salário", "Negócio", "Presente", "Extra", "Outros"]


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
        balance REAL NOT NULL DEFAULT 0,
        goal REAL NOT NULL DEFAULT 0,
        created_at TEXT,
        ref_source TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        tx_type TEXT NOT NULL DEFAULT 'saida',
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT,
        created_at TEXT NOT NULL,
        ref TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    if not column_exists(conn, "users", "created_at"):
        cur.execute("ALTER TABLE users ADD COLUMN created_at TEXT")
        conn.commit()

    if not column_exists(conn, "users", "ref_source"):
        cur.execute("ALTER TABLE users ADD COLUMN ref_source TEXT")
        conn.commit()

    if not column_exists(conn, "transactions", "tx_type"):
        cur.execute("ALTER TABLE transactions ADD COLUMN tx_type TEXT NOT NULL DEFAULT 'saida'")
        conn.commit()

    cur.execute("SELECT id FROM users WHERE username = ?", ("founder",))
    founder = cur.fetchone()

    if not founder:
        cur.execute("""
        INSERT INTO users (username, password, name, balance, goal, created_at, ref_source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "founder",
            "1234",
            "Roque Ntchiendo",
            1250000.0,
            200000.0,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "system"
        ))
        conn.commit()

    conn.close()


def generate_ref():
    return f"NB-{random.randint(100000, 999999)}"


def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user


def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user


def create_user(name, username, password, balance=0.0, ref_source="direct"):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO users (name, username, password, balance, goal, created_at, ref_source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        username,
        password,
        balance,
        0.0,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        ref_source
    ))
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


def add_transaction(user_id, tx_type, amount, category, note):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO transactions (user_id, tx_type, amount, category, note, created_at, ref)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        tx_type,
        amount,
        category,
        note,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        generate_ref()
    ))
    conn.commit()
    conn.close()


def update_balance(user_id, new_balance):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()


def update_goal(user_id, new_goal):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET goal = ? WHERE id = ?", (new_goal, user_id))
    conn.commit()
    conn.close()


def save_feedback(user_id, rating, message):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO feedback (user_id, rating, message, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        rating,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def get_feedback_summary():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total_feedback FROM feedback")
    total_feedback = cur.fetchone()["total_feedback"]

    cur.execute("SELECT AVG(rating) AS avg_rating FROM feedback")
    avg_rating_row = cur.fetchone()
    avg_rating = avg_rating_row["avg_rating"] if avg_rating_row["avg_rating"] is not None else 0

    cur.execute("""
    SELECT f.*, u.username
    FROM feedback f
    LEFT JOIN users u ON f.user_id = u.id
    ORDER BY f.id DESC
    LIMIT 10
    """)
    recent_feedback = cur.fetchall()

    conn.close()

    return {
        "total_feedback": total_feedback,
        "avg_rating": round(avg_rating, 2),
        "recent_feedback": recent_feedback
    }


def get_admin_stats():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cur.fetchone()["total_users"]

    cur.execute("SELECT COUNT(*) AS total_transactions FROM transactions")
    total_transactions = cur.fetchone()["total_transactions"]

    cur.execute("""
    SELECT COALESCE(SUM(amount), 0) AS total_income
    FROM transactions
    WHERE tx_type = 'entrada'
    """)
    total_income = cur.fetchone()["total_income"]

    cur.execute("""
    SELECT COALESCE(SUM(amount), 0) AS total_expense
    FROM transactions
    WHERE tx_type = 'saida'
    """)
    total_expense = cur.fetchone()["total_expense"]

    cur.execute("""
    SELECT id, name, username, balance, created_at, ref_source
    FROM users
    ORDER BY id DESC
    LIMIT 10
    """)
    recent_users = cur.fetchall()

    cur.execute("""
    SELECT id, tx_type, amount, category, note, created_at, ref, user_id
    FROM transactions
    ORDER BY id DESC
    LIMIT 15
    """)
    recent_transactions = cur.fetchall()

    cur.execute("""
    SELECT COALESCE(ref_source, 'direct') AS ref_source, COUNT(*) AS total
    FROM users
    GROUP BY COALESCE(ref_source, 'direct')
    ORDER BY total DESC, ref_source ASC
    """)
    source_breakdown = cur.fetchall()

    conn.close()

    feedback_summary = get_feedback_summary()

    return {
        "total_users": total_users,
        "total_transactions": total_transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "recent_users": recent_users,
        "recent_transactions": recent_transactions,
        "source_breakdown": source_breakdown,
        "total_feedback": feedback_summary["total_feedback"],
        "avg_rating": feedback_summary["avg_rating"],
        "recent_feedback": feedback_summary["recent_feedback"]
    }


def month_prefix():
    return datetime.now().strftime("%Y-%m")


def get_category_totals(transactions):
    totals = {category: 0.0 for category in EXPENSE_CATEGORIES}
    for tx in transactions:
        if tx["tx_type"] == "saida":
            cat = tx["category"]
            if cat in totals:
                totals[cat] += tx["amount"]
            else:
                totals["Outros"] += tx["amount"]
    return totals


def get_monthly_income(transactions):
    prefix = month_prefix()
    return sum(
        tx["amount"]
        for tx in transactions
        if tx["tx_type"] == "entrada" and tx["created_at"].startswith(prefix)
    )


def get_monthly_expense(transactions):
    prefix = month_prefix()
    return sum(
        tx["amount"]
        for tx in transactions
        if tx["tx_type"] == "saida" and tx["created_at"].startswith(prefix)
    )


def get_projected_expense(transactions):
    prefix = month_prefix()
    month_expenses = [
        tx for tx in transactions
        if tx["tx_type"] == "saida" and tx["created_at"].startswith(prefix)
    ]

    if not month_expenses:
        return 0.0

    today = datetime.now()
    current_day = max(today.day, 1)
    _, days_in_month = calendar.monthrange(today.year, today.month)

    spent_so_far = sum(tx["amount"] for tx in month_expenses)
    average_daily = spent_so_far / current_day
    projected = average_daily * days_in_month
    return round(projected, 2)


def get_days_left_in_month():
    today = datetime.now()
    _, days_in_month = calendar.monthrange(today.year, today.month)
    return days_in_month - today.day


def get_projected_final_balance(balance, monthly_expense):
    days_left = get_days_left_in_month()
    current_day = max(datetime.now().day, 1)

    if monthly_expense <= 0:
        return round(balance, 2)

    average_daily = monthly_expense / current_day
    projected_balance = balance - (average_daily * days_left)

    return round(projected_balance, 2)


def get_financial_autonomy(balance, monthly_expense):
    current_day = max(datetime.now().day, 1)

    if monthly_expense <= 0:
        return "Sem consumo suficiente"

    average_daily = monthly_expense / current_day
    if average_daily <= 0:
        return "Sem consumo suficiente"

    autonomy_days = balance / average_daily

    if autonomy_days >= 365:
        years = autonomy_days / 365
        return f"{int(autonomy_days)} dias (~{years:.1f} anos)"
    return f"{int(autonomy_days)} dias"


def get_financial_score(balance, monthly_income, monthly_expense, goal):
    score = 100

    if monthly_income <= 0 and monthly_expense > 0:
        score -= 35
    elif monthly_income > 0:
        ratio = monthly_expense / monthly_income

        if ratio > 1.2:
            score -= 35
        elif ratio > 1.0:
            score -= 25
        elif ratio > 0.8:
            score -= 15
        elif ratio > 0.6:
            score -= 8

    if goal > 0:
        if monthly_expense >= goal:
            score -= 20
        elif monthly_expense >= goal * 0.8:
            score -= 10

    if balance <= 0:
        score -= 30
    elif balance < 10000:
        score -= 20
    elif balance < 50000:
        score -= 10

    score = max(0, min(100, score))

    if score >= 80:
        status = "Forte 🟢"
    elif score >= 50:
        status = "Estável 🟡"
    else:
        status = "Crítico 🔴"

    return score, status


def get_alerts(category_totals, monthly_income, monthly_expense, projected_expense, goal, balance, days_left):
    alerts = []

    if monthly_income == 0 and monthly_expense == 0:
        alerts.append("Sem dados suficientes para auditoria.")
        return alerts

    if monthly_expense > 0:
        top_category = max(category_totals, key=category_totals.get)
        top_value = category_totals[top_category]
        top_percent = (top_value / monthly_expense) * 100 if monthly_expense > 0 else 0

        alerts.append(f"Maior categoria de gasto: {top_category} ({top_percent:.0f}%).")

        if top_percent >= 50:
            alerts.append(f"Atenção: mais de 50% dos teus gastos estão em {top_category}.")

    if monthly_income > 0 and monthly_expense > monthly_income:
        alerts.append("⚠️ Estás a gastar mais do que estás a receber neste mês.")

    if monthly_income > 0 and projected_expense > monthly_income:
        alerts.append("⚠️ Mantendo este ritmo, vais fechar o mês no vermelho.")

    if goal > 0:
        if monthly_expense >= goal:
            alerts.append("⚠️ Já atingiste ou ultrapassaste a tua meta financeira.")
        elif monthly_expense >= goal * 0.8:
            alerts.append("⚠️ Já consumiste mais de 80% da tua meta financeira.")

    if days_left > 0 and monthly_expense > 0:
        average_daily = monthly_expense / max(datetime.now().day, 1)
        projected_balance = balance - (average_daily * days_left)

        if projected_balance < 0:
            alerts.append("🚨 O teu saldo projetado para o fim do mês está negativo.")
        elif projected_balance < 10000:
            alerts.append("⚠️ O teu saldo projetado para o fim do mês está muito baixo.")

    return alerts


def get_categories_for_type(tx_type):
    return INCOME_CATEGORIES if tx_type == "entrada" else EXPENSE_CATEGORIES


PAGE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUVIBANK Lite Nível 2</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1220;
            color: #ffffff;
        }
        .wrap {
            max-width: 860px;
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
        .brand {
            font-size: 24px;
            font-weight: bold;
            color: #7fb3ff;
        }
        .muted {
            color: #b3bfd1;
            font-size: 14px;
        }
        .balance {
            font-size: 30px;
            font-weight: bold;
            margin: 8px 0;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        @media (min-width: 700px) {
            .grid {
                grid-template-columns: 1fr 1fr;
            }
        }
        input, select, textarea, button {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin-top: 10px;
            border-radius: 10px;
            border: none;
            font-size: 15px;
        }
        textarea {
            min-height: 110px;
            resize: vertical;
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
        .small {
            font-size: 13px;
            color: #b3bfd1;
        }
        .logout {
            color: #ffb0b0;
            text-decoration: none;
        }
        ul {
            padding-left: 18px;
        }
        .progress-box {
            background: #0b1220;
            border-radius: 12px;
            overflow: hidden;
            margin-top: 10px;
            border: 1px solid #22304a;
        }
        .progress-bar {
            height: 14px;
            background: #2f80ed;
        }
        .score {
            font-size: 26px;
            font-weight: bold;
            color: #7fffb0;
        }
        a.action-link {
            color: #7fb3ff;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="wrap">
    {% if page == 'login' %}
        <div class="card">
            <div class="brand">NUVIBANK Lite</div>
            <p class="muted">Controlo financeiro pessoal inteligente.</p>
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
                <input type="hidden" name="ref_source" value="{{ ref_source }}">
                <input name="name" placeholder="Nome completo" required>
                <input name="username" placeholder="Novo utilizador" required>
                <input name="password" type="password" placeholder="Nova senha" required>
                <input name="balance" placeholder="Saldo inicial (opcional)">
                <button type="submit">Criar conta</button>
            </form>
            <div class="small">Origem atual: {{ ref_source }}</div>
            {% if register_error %}
                <div class="error">{{ register_error }}</div>
            {% endif %}
            {% if register_message %}
                <div class="success">{{ register_message }}</div>
            {% endif %}
        </div>
    {% endif %}

    {% if page == 'dashboard' %}
        <div class="card">
            <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                <div>
                    <div class="brand">NUVIBANK Lite Nível 2</div>
                    <div class="muted">Sistema simples de controlo financeiro</div>
                </div>
                <div class="small">
                    {{ name }}<br>
                    <a class="logout" href="/logout">Terminar sessão</a>
                </div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Saldo Atual</h3>
                <div class="balance">{{ balance }} Kz</div>
                <div class="small">Utilizador: {{ username }}</div>
            </div>

            <div class="card">
                <h3>Score Financeiro</h3>
                <div class="score">{{ score }}/100</div>
                <div class="small">Status: <strong>{{ score_status }}</strong></div>
                <div class="small">Baseado em saldo, entradas, saídas e meta.</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Resumo do Mês</h3>
                <div><strong>Entradas:</strong> {{ monthly_income }} Kz</div>
                <div><strong>Saídas:</strong> {{ monthly_expense }} Kz</div>
                <div><strong>Projeção de gastos:</strong> {{ projected_expense }} Kz</div>
                <div><strong>Saldo projetado no fim do mês:</strong> {{ projected_final_balance }} Kz</div>
                <div><strong>Autonomia financeira:</strong> {{ autonomy_text }}</div>
                <div><strong>Dias restantes:</strong> {{ days_left }}</div>
            </div>

            <div class="card">
                <h3>Meta Financeira</h3>
                <div><strong>Meta:</strong> {{ goal }} Kz</div>
                <div><strong>Progresso:</strong> {{ progress_percent }}%</div>
                <div class="progress-box">
                    <div class="progress-bar" style="width: {{ progress_bar_width }}%;"></div>
                </div>
            </div>
        </div>

        <div class="card">
            <h3>Registar Movimento</h3>
            <form method="post" action="/add">
                <select name="tx_type" required>
                    <option value="saida">Saída</option>
                    <option value="entrada">Entrada</option>
                </select>
                <input name="amount" placeholder="Valor em Kz" required>
                <select name="category" required>
                    {% for c in categories %}
                        <option value="{{ c }}">{{ c }}</option>
                    {% endfor %}
                </select>
                <input name="note" placeholder="Nota opcional">
                <button type="submit">Guardar Movimento</button>
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
                {% for k, v in category_totals.items() %}
                    <li>{{ k }}: {{ v }} Kz</li>
                {% endfor %}
            </ul>
        </div>

        <div class="card">
            <h3>Alertas Inteligentes</h3>
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
                            {{ "Entrada" if tx["tx_type"] == "entrada" else "Saída" }} |
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
                <p class="muted">Nenhum movimento registado ainda.</p>
            {% endif %}
        </div>

        <div class="card">
            <h3>Feedback</h3>
            <p class="small">Ajuda-nos a melhorar o produto.</p>
            <a class="action-link" href="/feedback">💬 Dar feedback</a>
        </div>
    {% endif %}

    {% if page == 'feedback' %}
        <div class="card">
            <div class="brand">Feedback</div>
            <p class="muted">Conta-nos o que achaste da app.</p>

            <form method="post" action="/feedback">
                <select name="rating" required>
                    <option value="">Seleciona uma avaliação</option>
                    <option value="1">1 - Muito fraco</option>
                    <option value="2">2 - Fraco</option>
                    <option value="3">3 - Médio</option>
                    <option value="4">4 - Bom</option>
                    <option value="5">5 - Excelente</option>
                </select>

                <textarea name="message" placeholder="Escreve o teu feedback..." required></textarea>
                <button type="submit">Enviar Feedback</button>
            </form>

            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
            {% if message %}
                <div class="success">{{ message }}</div>
            {% endif %}

            <p class="small"><a class="action-link" href="/dashboard">← Voltar ao dashboard</a></p>
        </div>
    {% endif %}
</div>
</body>
</html>
"""


ADMIN_PAGE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUVIBANK Admin</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1220;
            color: #ffffff;
        }
        .wrap {
            max-width: 960px;
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
        .brand {
            font-size: 24px;
            font-weight: bold;
            color: #7fb3ff;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        @media (min-width: 700px) {
            .grid {
                grid-template-columns: 1fr 1fr;
            }
        }
        input, button {
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
        .metric {
            font-size: 28px;
            font-weight: bold;
            margin-top: 8px;
        }
        .small {
            color: #b3bfd1;
            font-size: 13px;
        }
        .error {
            background: #4a1f28;
            color: #ffb3b3;
            padding: 10px;
            border-radius: 10px;
            margin-top: 12px;
        }
        .logout {
            color: #ffb0b0;
            text-decoration: none;
        }
        ul {
            padding-left: 18px;
        }
    </style>
</head>
<body>
<div class="wrap">
    {% if page == 'admin_login' %}
        <div class="card">
            <div class="brand">NUVIBANK Admin</div>
            <p class="small">Área restrita do fundador.</p>
            <form method="post" action="/admin-login">
                <input name="password" type="password" placeholder="Senha admin" required>
                <button type="submit">Entrar no Admin</button>
            </form>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </div>
    {% endif %}

    {% if page == 'admin_dashboard' %}
        <div class="card">
            <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                <div>
                    <div class="brand">NUVIBANK Admin Dashboard</div>
                    <div class="small">Painel interno de validação e crescimento</div>
                </div>
                <div class="small">
                    <a class="logout" href="/admin-logout">Sair do Admin</a>
                </div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Total de Utilizadores</h3>
                <div class="metric">{{ total_users }}</div>
            </div>

            <div class="card">
                <h3>Total de Movimentos</h3>
                <div class="metric">{{ total_transactions }}</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Total de Entradas</h3>
                <div class="metric">{{ total_income }} Kz</div>
            </div>

            <div class="card">
                <h3>Total de Saídas</h3>
                <div class="metric">{{ total_expense }} Kz</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>Total de Feedbacks</h3>
                <div class="metric">{{ total_feedback }}</div>
            </div>

            <div class="card">
                <h3>Média de Rating</h3>
                <div class="metric">{{ avg_rating }}/5</div>
            </div>
        </div>

        <div class="card">
            <h3>Aquisição por Origem</h3>
            {% if source_breakdown %}
                <ul>
                    {% for s in source_breakdown %}
                        <li>{{ s["ref_source"] }}: {{ s["total"] }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="small">Sem dados de origem.</p>
            {% endif %}
        </div>

        <div class="card">
            <h3>Últimos Utilizadores</h3>
            {% if recent_users %}
                <ul>
                    {% for u in recent_users %}
                        <li>{{ u["created_at"] }} | {{ u["name"] }} | {{ u["username"] }} | {{ u["balance"] }} Kz | origem: {{ u["ref_source"] or "direct" }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="small">Sem utilizadores recentes.</p>
            {% endif %}
        </div>

        <div class="card">
            <h3>Últimos Movimentos</h3>
            {% if recent_transactions %}
                <ul>
                    {% for t in recent_transactions %}
                        <li>{{ t["created_at"] }} | {{ "Entrada" if t["tx_type"] == "entrada" else "Saída" }} | {{ t["category"] }} | {{ t["amount"] }} Kz | {{ t["ref"] }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="small">Sem movimentos recentes.</p>
            {% endif %}
        </div>

        <div class="card">
            <h3>Últimos Feedbacks</h3>
            {% if recent_feedback %}
                <ul>
                    {% for f in recent_feedback %}
                        <li>{{ f["created_at"] }} | {{ f["username"] }} | {{ f["rating"] }}/5 | {{ f["message"] }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="small">Sem feedback recente.</p>
            {% endif %}
        </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.before_request
def capture_ref():
    ref = request.args.get("ref", "").strip()
    if ref:
        session["ref_source"] = ref


def render_login(error=None, register_error=None, register_message=None):
    return render_template_string(
        PAGE,
        page="login",
        error=error,
        register_error=register_error,
        register_message=register_message,
        ref_source=session.get("ref_source", "direct")
    )


def render_feedback(error=None, message=None):
    return render_template_string(
        PAGE,
        page="feedback",
        error=error,
        message=message
    )


def render_dashboard(user_row, error=None, message=None):
    transactions = get_transactions(user_row["id"])

    category_totals = get_category_totals(transactions)
    monthly_income = get_monthly_income(transactions)
    monthly_expense = get_monthly_expense(transactions)
    projected_expense = get_projected_expense(transactions)
    goal = user_row["goal"] if user_row["goal"] is not None else 0.0
    days_left = get_days_left_in_month()
    projected_final_balance = get_projected_final_balance(user_row["balance"], monthly_expense)
    autonomy_text = get_financial_autonomy(user_row["balance"], monthly_expense)

    alerts = get_alerts(
        category_totals,
        monthly_income,
        monthly_expense,
        projected_expense,
        goal,
        user_row["balance"],
        days_left
    )

    score, score_status = get_financial_score(
        user_row["balance"],
        monthly_income,
        monthly_expense,
        goal
    )

    progress_percent = 0
    if goal > 0:
        progress_percent = int((monthly_expense / goal) * 100)

    progress_bar_width = min(progress_percent, 100)

    return render_template_string(
        PAGE,
        page="dashboard",
        name=user_row["name"],
        username=user_row["username"],
        balance=f"{user_row['balance']:,.2f}",
        monthly_income=f"{monthly_income:,.2f}",
        monthly_expense=f"{monthly_expense:,.2f}",
        projected_expense=f"{projected_expense:,.2f}",
        projected_final_balance=f"{projected_final_balance:,.2f}",
        autonomy_text=autonomy_text,
        goal=f"{goal:,.2f}",
        progress_percent=progress_percent,
        progress_bar_width=progress_bar_width,
        score=score,
        score_status=score_status,
        days_left=days_left,
        category_totals={k: f"{v:,.2f}" for k, v in category_totals.items()},
        alerts=alerts,
        transactions=transactions,
        categories=EXPENSE_CATEGORIES,
        error=error,
        message=message
    )


@app.route("/")
def home():
    if session.get("uid"):
        return redirect("/dashboard")
    return render_login()


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user_row = get_user_by_username(username)
    if not user_row or user_row["password"] != password:
        return render_login(error="Credenciais inválidas.")

    session["uid"] = user_row["id"]
    return redirect("/dashboard")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    balance_raw = request.form.get("balance", "").strip().replace(",", ".")
    form_ref = request.form.get("ref_source", "").strip()

    if not name or not username or not password:
        return render_login(register_error="Preenche nome, utilizador e senha.")

    if get_user_by_username(username):
        return render_login(register_error="Esse utilizador já existe.")

    balance = 0.0
    if balance_raw:
        try:
            balance = float(balance_raw)
        except ValueError:
            return render_login(register_error="Saldo inicial inválido.")

        if balance < 0:
            return render_login(register_error="O saldo inicial não pode ser negativo.")

    ref_source = form_ref or session.get("ref_source", "direct")
    create_user(name, username, password, balance, ref_source)

    return render_login(register_message="Conta criada com sucesso.")


@app.route("/dashboard")
def dashboard():
    if not session.get("uid"):
        return redirect("/")

    user_row = get_user_by_id(session["uid"])
    if not user_row:
        session.clear()
        return redirect("/")

    return render_dashboard(user_row)


@app.route("/add", methods=["POST"])
def add():
    if not session.get("uid"):
        return redirect("/")

    user_row = get_user_by_id(session["uid"])
    if not user_row:
        session.clear()
        return redirect("/")

    tx_type = request.form.get("tx_type", "").strip()
    amount_raw = request.form.get("amount", "").strip().replace(",", ".")
    category = request.form.get("category", "").strip()
    note = request.form.get("note", "").strip()

    if tx_type not in ["entrada", "saida"]:
        return render_dashboard(user_row, error="Tipo de movimento inválido.")

    if not amount_raw:
        return render_dashboard(user_row, error="O valor é obrigatório.")

    try:
        amount = float(amount_raw)
    except ValueError:
        return render_dashboard(user_row, error="Valor inválido. Introduz apenas números.")

    if amount <= 0:
        return render_dashboard(user_row, error="O valor deve ser maior que zero.")

    valid_categories = get_categories_for_type(tx_type)
    if category not in valid_categories:
        return render_dashboard(user_row, error="Categoria inválida para este tipo de movimento.")

    current_balance = user_row["balance"]

    if tx_type == "saida":
        if amount > current_balance:
            return render_dashboard(user_row, error="Saldo insuficiente para esta saída.")
        new_balance = current_balance - amount
    else:
        new_balance = current_balance + amount

    update_balance(user_row["id"], new_balance)
    add_transaction(user_row["id"], tx_type, amount, category, note)

    updated_user = get_user_by_id(user_row["id"])
    return render_dashboard(updated_user, message="Movimento registado com sucesso.")


@app.route("/goal", methods=["POST"])
def goal():
    if not session.get("uid"):
        return redirect("/")

    user_row = get_user_by_id(session["uid"])
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

    update_goal(user_row["id"], new_goal)
    updated_user = get_user_by_id(user_row["id"])
    return render_dashboard(updated_user, message="Meta guardada com sucesso.")


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if not session.get("uid"):
        return redirect("/")

    if request.method == "POST":
        rating_raw = request.form.get("rating", "").strip()
        message = request.form.get("message", "").strip()

        if not rating_raw:
            return render_feedback(error="Seleciona uma avaliação.")
        if not message:
            return render_feedback(error="Escreve o teu feedback.")

        try:
            rating = int(rating_raw)
        except ValueError:
            return render_feedback(error="Avaliação inválida.")

        if rating < 1 or rating > 5:
            return render_feedback(error="A avaliação deve estar entre 1 e 5.")

        save_feedback(session["uid"], rating, message)
        return render_feedback(message="Feedback enviado com sucesso.")

    return render_feedback()


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "").strip()

        if password != ADMIN_PASSWORD:
            return render_template_string(ADMIN_PAGE, page="admin_login", error="Senha admin inválida.")

        session["admin_ok"] = True
        return redirect("/admin")

    return render_template_string(ADMIN_PAGE, page="admin_login", error=None)


@app.route("/admin")
def admin_dashboard():
    if not session.get("admin_ok"):
        return redirect("/admin-login")

    stats = get_admin_stats()

    return render_template_string(
        ADMIN_PAGE,
        page="admin_dashboard",
        total_users=stats["total_users"],
        total_transactions=stats["total_transactions"],
        total_income=f"{stats['total_income']:,.2f}",
        total_expense=f"{stats['total_expense']:,.2f}",
        recent_users=stats["recent_users"],
        recent_transactions=stats["recent_transactions"],
        source_breakdown=stats["source_breakdown"],
        total_feedback=stats["total_feedback"],
        avg_rating=stats["avg_rating"],
        recent_feedback=stats["recent_feedback"]
    )


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_ok", None)
    return redirect("/admin-login")


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
