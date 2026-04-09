import os
import sqlite3
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:
    psycopg2 = None
    RealDictCursor = None


# =========================================================
# CONFIG
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, "nuvibank.db")

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123NUVI")

DB_ENGINE = "postgres" if DATABASE_URL else "sqlite"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


# =========================================================
# HELPERS
# =========================================================
def money(value):
    try:
        return f"{float(value):,.2f} Kz"
    except Exception:
        return "0.00 Kz"


def dtfmt(value):
    if not value:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    try:
        return str(value)[:16]
    except Exception:
        return "-"


app.jinja_env.filters["money"] = money
app.jinja_env.filters["dtfmt"] = dtfmt


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def get_db():
    if DB_ENGINE == "sqlite":
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    if psycopg2 is None:
        raise RuntimeError("psycopg2 não instalado.")
    return psycopg2.connect(normalize_database_url(DATABASE_URL))


def fetch_one(sqlite_sql, pg_sql, params=()):
    conn = get_db()
    try:
        if DB_ENGINE == "sqlite":
            cur = conn.execute(sqlite_sql, params)
            row = cur.fetchone()
            return dict(row) if row else None
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(pg_sql, params)
        return cur.fetchone()
    finally:
        conn.close()


def fetch_all(sqlite_sql, pg_sql, params=()):
    conn = get_db()
    try:
        if DB_ENGINE == "sqlite":
            cur = conn.execute(sqlite_sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(pg_sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def execute_write(sqlite_sql, pg_sql, params=()):
    conn = get_db()
    try:
        if DB_ENGINE == "sqlite":
            cur = conn.execute(sqlite_sql, params)
            conn.commit()
            return cur.lastrowid
        cur = conn.cursor()
        cur.execute(pg_sql, params)
        conn.commit()
        try:
            result = cur.fetchone()
            return result[0] if result else None
        except Exception:
            return None
    finally:
        conn.close()


def month_range():
    now = datetime.now()
    start = datetime(now.year, now.month, 1)
    if now.month == 12:
        end = datetime(now.year + 1, 1, 1)
    else:
        end = datetime(now.year, now.month + 1, 1)
    return start, end


def days_remaining_in_month():
    now = datetime.now()
    _, end = month_range()
    return max((end.date() - now.date()).days, 0)


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return fetch_one(
        "SELECT * FROM users WHERE id = ?",
        "SELECT * FROM users WHERE id = %s",
        (user_id,),
    )


def latest_goal(user_id):
    return fetch_one(
        "SELECT * FROM goals WHERE user_id = ?",
        "SELECT * FROM goals WHERE user_id = %s",
        (user_id,),
    )


def monthly_totals(user_id):
    start, end = month_range()
    rows = fetch_all(
        """
        SELECT movement_type, COALESCE(SUM(amount), 0) AS total
        FROM movements
        WHERE user_id = ? AND created_at >= ? AND created_at < ?
        GROUP BY movement_type
        """,
        """
        SELECT movement_type, COALESCE(SUM(amount), 0) AS total
        FROM movements
        WHERE user_id = %s AND created_at >= %s AND created_at < %s
        GROUP BY movement_type
        """,
        (user_id, start, end),
    )
    incoming = 0.0
    outgoing = 0.0
    for row in rows:
        if row["movement_type"] == "Entrada":
            incoming = float(row["total"] or 0)
        elif row["movement_type"] == "Saída":
            outgoing = float(row["total"] or 0)
    return incoming, outgoing


def category_summary(user_id):
    start, end = month_range()
    rows = fetch_all(
        """
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM movements
        WHERE user_id = ? AND movement_type = 'Saída'
          AND created_at >= ? AND created_at < ?
        GROUP BY category
        ORDER BY total DESC
        """,
        """
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM movements
        WHERE user_id = %s AND movement_type = 'Saída'
          AND created_at >= %s AND created_at < %s
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id, start, end),
    )

    base = {
        "Comida": 0.0,
        "Transporte": 0.0,
        "Casa": 0.0,
        "Lazer": 0.0,
        "Outros": 0.0,
    }
    for row in rows:
        cat = row["category"] or "Outros"
        base[cat] = float(row["total"] or 0)
    return base


def build_alerts(balance, incoming, outgoing, categories):
    alerts = []

    if outgoing <= 0:
        alerts.append("Sem dados suficientes para auditoria.")
        return alerts

    top_name, top_value = max(categories.items(), key=lambda x: x[1])
    if top_value > 0:
        share = (top_value / outgoing) * 100
        alerts.append(f"Maior categoria de gasto: {top_name} ({share:.0f}%).")
        if share > 50:
            alerts.append(f"Atenção: mais de 50% dos teus gastos estão em {top_name}.")

    if balance < 0:
        alerts.append("Saldo negativo. Precisam-se cortes imediatos.")
    elif outgoing > incoming and incoming > 0:
        alerts.append("Estás a gastar mais do que entra neste mês.")

    return alerts


def compute_projection(balance, outgoing):
    days_left = days_remaining_in_month()
    day_of_month = max(datetime.now().day, 1)
    avg_daily_spend = outgoing / day_of_month if day_of_month > 0 else 0
    projected_month_spend = avg_daily_spend * (day_of_month + days_left)
    projected_end_balance = balance - (projected_month_spend - outgoing)
    return projected_month_spend, projected_end_balance


def compute_autonomy(balance, outgoing):
    day_of_month = max(datetime.now().day, 1)
    avg_daily_spend = outgoing / day_of_month if day_of_month > 0 else 0

    if avg_daily_spend <= 0:
        return "Sem consumo suficiente"

    days = balance / avg_daily_spend if avg_daily_spend > 0 else 0
    if days < 365:
        return f"{days:.0f} dias"
    return f"{days:.0f} dias (~{days / 365:.1f} anos)"


def compute_score(balance, incoming, outgoing, goal_value):
    score = 50

    if balance > 0:
        score += 15
    if incoming > 0:
        score += 10
    if incoming >= outgoing and outgoing > 0:
        score += 15
    elif outgoing > incoming and incoming > 0:
        score -= 10

    if goal_value > 0:
        progress = min((balance / goal_value) * 100, 100)
        if progress >= 100:
            score += 10
        elif progress >= 50:
            score += 5

    score = max(0, min(100, int(score)))

    if score >= 80:
        status = "Forte 🟢"
    elif score >= 60:
        status = "Estável 🟡"
    else:
        status = "Frágil 🔴"

    return score, status


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Faz login para continuar.", "error")
            return redirect(url_for("index"))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_ok"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper


# =========================================================
# SCHEMA
# =========================================================
SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0,
    acquisition_source TEXT NOT NULL DEFAULT 'direct',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT,
    movement_code TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    monthly_goal REAL NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

POSTGRES_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    balance NUMERIC(18,2) NOT NULL DEFAULT 0,
    acquisition_source TEXT NOT NULL DEFAULT 'direct',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    movement_type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    note TEXT,
    movement_code TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    monthly_goal NUMERIC(18,2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    conn = get_db()
    try:
        if DB_ENGINE == "sqlite":
            conn.executescript(SQLITE_SCHEMA)
            conn.commit()
        else:
            cur = conn.cursor()
            cur.execute(POSTGRES_SCHEMA)
            conn.commit()
    finally:
        conn.close()


# =========================================================
# TEMPLATES
# =========================================================
BASE_STYLE = """
<style>
    :root{
        --bg:#071223;
        --card:#0b1730;
        --card-2:#0d1a35;
        --line:#1b2a4e;
        --text:#eaf1ff;
        --muted:#aeb8d0;
        --blue:#3b82f6;
        --blue-2:#60a5fa;
    }
    *{box-sizing:border-box}
    body{
        margin:0;
        font-family:Arial,Helvetica,sans-serif;
        background:var(--bg);
        color:var(--text);
        padding:24px 16px 40px;
    }
    .wrap{max-width:860px;margin:0 auto}
    .card{
        background:linear-gradient(180deg,var(--card),var(--card-2));
        border:1px solid var(--line);
        border-radius:24px;
        padding:24px;
        margin-bottom:22px;
    }
    h1,h2,h3{margin:0 0 12px}
    .brand{
        color:var(--blue-2);
        font-size:clamp(28px,5vw,44px);
        font-weight:800;
        margin-bottom:8px;
    }
    .sub{color:var(--muted);margin-bottom:22px}
    input,select,textarea{
        width:100%;
        border:none;
        outline:none;
        border-radius:16px;
        padding:16px 18px;
        font-size:18px;
        margin-bottom:14px;
        background:#f3f4f6;
        color:#111827;
    }
    textarea{min-height:120px;resize:vertical}
    button,.btn{
        display:inline-block;
        width:100%;
        border:none;
        border-radius:16px;
        padding:16px 18px;
        font-size:20px;
        font-weight:700;
        cursor:pointer;
        text-decoration:none;
        text-align:center;
        background:var(--blue);
        color:white;
    }
    .mini-link{
        color:#fca5a5;
        text-decoration:none;
        font-weight:700;
    }
    .flash{
        padding:14px 16px;
        border-radius:16px;
        margin-bottom:16px;
        font-weight:700;
    }
    .flash-success{background:rgba(34,197,94,.15);color:#bbf7d0;border:1px solid rgba(34,197,94,.3)}
    .flash-error{background:rgba(239,68,68,.15);color:#fecaca;border:1px solid rgba(239,68,68,.3)}
    .grid{display:grid;grid-template-columns:1fr;gap:18px}
    @media(min-width:760px){.grid.two{grid-template-columns:1fr 1fr}.grid.three{grid-template-columns:repeat(3,1fr)}}
    .stat{font-size:clamp(24px,5vw,54px);font-weight:800;margin:8px 0 10px}
    .muted{color:var(--muted)}
    ul.clean{margin:0;padding-left:20px;line-height:1.6}
    .progress{width:100%;height:20px;border-radius:999px;border:1px solid var(--line);background:#081120;overflow:hidden;margin-top:12px}
    .progress > div{height:100%;background:linear-gradient(90deg,var(--blue),var(--blue-2))}
    table{width:100%;border-collapse:collapse;font-size:14px}
    th,td{padding:10px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
    .tag{display:inline-block;padding:6px 10px;border-radius:999px;background:#102142;border:1px solid var(--line);color:#dbeafe;font-size:12px;font-weight:700}
</style>
"""

INDEX_TEMPLATE = BASE_STYLE + """
<div class="wrap">
    <div class="card">
        <div class="brand">NUVIBANK Lite</div>
        <div class="sub">Controlo financeiro pessoal inteligente.</div>

        {% with messages = get_flashed_messages(with_categories=true) %}
          {% for category, message in messages %}
            <div class="flash flash-{{category}}">{{ message }}</div>
          {% endfor %}
        {% endwith %}

        <div class="grid two">
            <div class="card" style="margin:0">
                <h2>Entrar</h2>
                <form method="post" action="{{ url_for('login') }}">
                    <input type="text" name="username" placeholder="Utilizador" required>
                    <input type="password" name="password" placeholder="Senha" required>
                    <button type="submit">Entrar</button>
                </form>
            </div>

            <div class="card" style="margin:0">
                <h2>Criar conta</h2>
                <form method="post" action="{{ url_for('register') }}">
                    <input type="text" name="full_name" placeholder="Nome completo" required>
                    <input type="email" name="email" placeholder="Email (opcional)">
                    <input type="text" name="username" placeholder="Novo utilizador" required>
                    <input type="password" name="password" placeholder="Nova senha" required>
                    <input type="number" step="0.01" name="balance" placeholder="Saldo inicial (opcional)">
                    <button type="submit">Criar conta</button>
                </form>
                <div class="muted">Origem atual: {{ acquisition_source }}</div>
            </div>
        </div>
    </div>
</div>
"""

APP_TEMPLATE = BASE_STYLE + """
<div class="wrap">
    <div class="card">
        <div class="brand">NUVIBANK Lite Nível 2</div>
        <div class="sub">Sistema simples de controlo financeiro</div>
        <div style="font-size:18px">{{ user.full_name }}</div>
        <a class="mini-link" href="{{ url_for('logout') }}">Terminar sessão</a>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% for category, message in messages %}
        <div class="flash flash-{{category}}">{{ message }}</div>
      {% endfor %}
    {% endwith %}

    <div class="card">
        <h2>Saldo Atual</h2>
        <div class="stat">{{ user.balance|money }}</div>
        <div class="muted">Utilizador: {{ user.username }}</div>
    </div>

    <div class="card">
        <h2>Score Financeiro</h2>
        <div class="stat" style="color:#6ee7b7">{{ score }}/100</div>
        <div class="muted">Status: <strong>{{ score_status }}</strong></div>
        <div class="muted">Baseado em saldo, entradas, saídas e meta.</div>
    </div>

    <div class="card">
        <h2>Resumo do Mês</h2>
        <div><strong>Entradas:</strong> {{ incoming|money }}</div>
        <div><strong>Saídas:</strong> {{ outgoing|money }}</div>
        <div><strong>Projeção de gastos:</strong> {{ projected_spend|money }}</div>
        <div><strong>Saldo projetado no fim do mês:</strong> {{ projected_balance|money }}</div>
        <div><strong>Autonomia financeira:</strong> {{ autonomy }}</div>
        <div><strong>Dias restantes:</strong> {{ days_left }}</div>
    </div>

    <div class="card">
        <h2>Meta Financeira</h2>
        <div><strong>Meta:</strong> {{ goal_value|money }}</div>
        <div><strong>Progresso:</strong> {{ goal_progress }}%</div>
        <div class="progress"><div style="width:{{ goal_progress }}%"></div></div>
    </div>

    <div class="grid two">
        <div class="card">
            <h2>Registar Movimento</h2>
            <form method="post" action="{{ url_for('save_movement') }}">
                <select name="movement_type" required>
                    <option value="Saída">Saída</option>
                    <option value="Entrada">Entrada</option>
                </select>

                <input type="number" step="0.01" name="amount" placeholder="Valor em Kz" required>

                <select name="category" required>
                    <option value="Comida">Comida</option>
                    <option value="Transporte">Transporte</option>
                    <option value="Casa">Casa</option>
                    <option value="Lazer">Lazer</option>
                    <option value="Outros">Outros</option>
                </select>

                <input type="text" name="note" placeholder="Nota opcional">
                <button type="submit">Guardar Movimento</button>
            </form>
        </div>

        <div class="card">
            <h2>Definir Meta</h2>
            <form method="post" action="{{ url_for('save_goal') }}">
                <input type="number" step="0.01" name="goal_value" placeholder="Meta mensal em Kz" required>
                <button type="submit">Guardar Meta</button>
            </form>
        </div>
    </div>

    <div class="card">
        <h2>Resumo por Categoria</h2>
        <ul class="clean">
            <li>Comida: {{ categories['Comida']|money }}</li>
            <li>Transporte: {{ categories['Transporte']|money }}</li>
            <li>Casa: {{ categories['Casa']|money }}</li>
            <li>Lazer: {{ categories['Lazer']|money }}</li>
            <li>Outros: {{ categories['Outros']|money }}</li>
        </ul>
    </div>

    <div class="card">
        <h2>Alertas Inteligentes</h2>
        <ul class="clean">
            {% for item in alerts %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    </div>

    <div class="card">
        <h2>Histórico</h2>
        {% if movements %}
            <ul class="clean">
                {% for m in movements %}
                    <li>
                        {{ m.created_at|dtfmt }} |
                        {{ m.movement_type }} |
                        {{ m.category }} |
                        {{ m.amount|money }} |
                        {{ m.movement_code }} |
                        {{ m.note or '-' }}
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="muted">Nenhum movimento registado ainda.</div>
        {% endif %}
    </div>

    <div class="card">
        <h2>Feedback</h2>
        <div class="sub">Ajuda-nos a melhorar o produto.</div>
        <form method="post" action="{{ url_for('save_feedback') }}">
            <textarea name="message" placeholder="Escreve o teu feedback..." required></textarea>
            <button type="submit">Dar feedback</button>
        </form>

        {% if my_feedback %}
            <h3 style="margin-top:24px">Meus feedbacks</h3>
            <ul class="clean">
                {% for fb in my_feedback %}
                    <li>{{ fb.created_at|dtfmt }} — {{ fb.message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
</div>
"""

ADMIN_LOGIN_TEMPLATE = BASE_STYLE + """
<div class="wrap">
    <div class="card">
        <div class="brand">NUVIBANK Admin</div>
        <div class="sub">Área restrita do fundador.</div>

        {% with messages = get_flashed_messages(with_categories=true) %}
          {% for category, message in messages %}
            <div class="flash flash-{{category}}">{{ message }}</div>
          {% endfor %}
        {% endwith %}

        <form method="post">
            <input type="password" name="password" placeholder="Senha admin" required>
            <button type="submit">Entrar no Admin</button>
        </form>
    </div>
</div>
"""

ADMIN_TEMPLATE = BASE_STYLE + """
<div class="wrap">
    <div class="card">
        <div class="brand">NUVIBANK Admin</div>
        <div class="sub">Controlo central do sistema.</div>
        <a class="mini-link" href="{{ url_for('admin_logout') }}">Terminar sessão admin</a>
    </div>

    <div class="grid three">
        <div class="card">
            <h3>Utilizadores</h3>
            <div class="stat">{{ total_users }}</div>
        </div>
        <div class="card">
            <h3>Movimentos</h3>
            <div class="stat">{{ total_movements }}</div>
        </div>
        <div class="card">
            <h3>Feedbacks</h3>
            <div class="stat">{{ total_feedback }}</div>
        </div>
    </div>

    <div class="card">
        <h2>Utilizadores</h2>
        <div style="overflow:auto">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Utilizador</th>
                        <th>Saldo</th>
                        <th>Origem</th>
                        <th>Criado</th>
                    </tr>
                </thead>
                <tbody>
                    {% for u in users %}
                    <tr>
                        <td>{{ u.id }}</td>
                        <td>{{ u.full_name }}</td>
                        <td>{{ u.email or '-' }}</td>
                        <td>{{ u.username }}</td>
                        <td>{{ u.balance|money }}</td>
                        <td><span class="tag">{{ u.acquisition_source }}</span></td>
                        <td>{{ u.created_at|dtfmt }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <div class="card">
        <h2>Últimos feedbacks</h2>
        {% if feedbacks %}
            <div style="overflow:auto">
                <table>
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Utilizador</th>
                            <th>Mensagem</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for fb in feedbacks %}
                        <tr>
                            <td>{{ fb.created_at|dtfmt }}</td>
                            <td>{{ fb.username or 'anónimo' }}</td>
                            <td>{{ fb.message }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="muted">Sem feedbacks ainda.</div>
        {% endif %}
    </div>

    <div class="card">
        <h2>Últimos movimentos</h2>
        {% if movements %}
            <div style="overflow:auto">
                <table>
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>Utilizador</th>
                            <th>Tipo</th>
                            <th>Categoria</th>
                            <th>Valor</th>
                            <th>Código</th>
                            <th>Nota</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for m in movements %}
                        <tr>
                            <td>{{ m.created_at|dtfmt }}</td>
                            <td>{{ m.username }}</td>
                            <td>{{ m.movement_type }}</td>
                            <td>{{ m.category }}</td>
                            <td>{{ m.amount|money }}</td>
                            <td>{{ m.movement_code }}</td>
                            <td>{{ m.note or '-' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="muted">Sem movimentos ainda.</div>
        {% endif %}
    </div>
</div>
"""


# =========================================================
# ROUTES
# =========================================================
@app.before_request
def track_source():
    ref = request.args.get("ref", "").strip()
    if ref:
        session["acquisition_source"] = ref
    elif "acquisition_source" not in session:
        session["acquisition_source"] = "direct"


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("app_dashboard"))
    return render_template_string(
        INDEX_TEMPLATE,
        acquisition_source=session.get("acquisition_source", "direct"),
    )


@app.route("/register", methods=["POST"])
def register():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip() or None
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    balance_raw = request.form.get("balance", "").strip()

    if not full_name or not username or not password:
        flash("Preenche nome, utilizador e senha.", "error")
        return redirect(url_for("index"))

    existing = fetch_one(
        "SELECT id FROM users WHERE username = ?",
        "SELECT id FROM users WHERE username = %s",
        (username,),
    )
    if existing:
        flash("Esse utilizador já existe.", "error")
        return redirect(url_for("index"))

    try:
        balance = float(balance_raw) if balance_raw else 0.0
    except ValueError:
        balance = 0.0

    password_hash = generate_password_hash(password)
    source = session.get("acquisition_source", "direct")

    if DB_ENGINE == "sqlite":
        execute_write(
            """
            INSERT INTO users (full_name, email, username, password_hash, balance, acquisition_source)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            "",
            (full_name, email, username, password_hash, balance, source),
        )
    else:
        execute_write(
            "",
            """
            INSERT INTO users (full_name, email, username, password_hash, balance, acquisition_source)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (full_name, email, username, password_hash, balance, source),
        )

    user = fetch_one(
        "SELECT * FROM users WHERE username = ?",
        "SELECT * FROM users WHERE username = %s",
        (username,),
    )
    session["user_id"] = user["id"]
    flash("Conta criada com sucesso.", "success")
    return redirect(url_for("app_dashboard"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user = fetch_one(
        "SELECT * FROM users WHERE username = ?",
        "SELECT * FROM users WHERE username = %s",
        (username,),
    )
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Utilizador ou senha inválidos.", "error")
        return redirect(url_for("index"))

    session["user_id"] = user["id"]
    flash("Sessão iniciada com sucesso.", "success")
    return redirect(url_for("app_dashboard"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Sessão terminada.", "success")
    return redirect(url_for("index"))


@app.route("/app")
@login_required
def app_dashboard():
    user = current_user()
    goal = latest_goal(user["id"])
    goal_value = float(goal["monthly_goal"]) if goal else 0.0

    incoming, outgoing = monthly_totals(user["id"])
    categories = category_summary(user["id"])
    alerts = build_alerts(float(user["balance"]), incoming, outgoing, categories)
    projected_spend, projected_balance = compute_projection(float(user["balance"]), outgoing)
    autonomy = compute_autonomy(float(user["balance"]), outgoing)
    score, score_status = compute_score(float(user["balance"]), incoming, outgoing, goal_value)

    goal_progress = 0
    if goal_value > 0:
        goal_progress = min(int((float(user["balance"]) / goal_value) * 100), 100)

    movements = fetch_all(
        """
        SELECT * FROM movements
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 20
        """,
        """
        SELECT * FROM movements
        WHERE user_id = %s
        ORDER BY created_at DESC, id DESC
        LIMIT 20
        """,
        (user["id"],),
    )

    my_feedback = fetch_all(
        """
        SELECT * FROM feedback
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 20
        """,
        """
        SELECT * FROM feedback
        WHERE user_id = %s
        ORDER BY created_at DESC, id DESC
        LIMIT 20
        """,
        (user["id"],),
    )

    return render_template_string(
        APP_TEMPLATE,
        user=user,
        score=score,
        score_status=score_status,
        incoming=incoming,
        outgoing=outgoing,
        projected_spend=projected_spend,
        projected_balance=projected_balance,
        autonomy=autonomy,
        days_left=days_remaining_in_month(),
        goal_value=goal_value,
        goal_progress=goal_progress,
        categories=categories,
        alerts=alerts,
        movements=movements,
        my_feedback=my_feedback,
    )


@app.route("/movement", methods=["POST"])
@login_required
def save_movement():
    user = current_user()
    movement_type = request.form.get("movement_type", "").strip()
    category = request.form.get("category", "").strip()
    note = request.form.get("note", "").strip()
    amount_raw = request.form.get("amount", "").strip()

    try:
        amount = float(amount_raw)
    except ValueError:
        flash("Valor inválido.", "error")
        return redirect(url_for("app_dashboard"))

    if amount <= 0:
        flash("O valor deve ser maior que zero.", "error")
        return redirect(url_for("app_dashboard"))

    code = f"NB-{str(uuid.uuid4().int)[:6]}"

    if movement_type == "Entrada":
        new_balance = float(user["balance"]) + amount
    else:
        new_balance = float(user["balance"]) - amount

    execute_write(
        """
        INSERT INTO movements (user_id, movement_type, category, amount, note, movement_code)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        """
        INSERT INTO movements (user_id, movement_type, category, amount, note, movement_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user["id"], movement_type, category, amount, note or None, code),
    )

    execute_write(
        "UPDATE users SET balance = ? WHERE id = ?",
        "UPDATE users SET balance = %s WHERE id = %s",
        (new_balance, user["id"]),
    )

    flash("Movimento guardado com sucesso.", "success")
    return redirect(url_for("app_dashboard"))


@app.route("/goal", methods=["POST"])
@login_required
def save_goal():
    user = current_user()
    goal_raw = request.form.get("goal_value", "").strip()

    try:
        goal_value = float(goal_raw)
    except ValueError:
        flash("Meta inválida.", "error")
        return redirect(url_for("app_dashboard"))

    if goal_value < 0:
        flash("A meta não pode ser negativa.", "error")
        return redirect(url_for("app_dashboard"))

    if DB_ENGINE == "sqlite":
        execute_write(
            """
            INSERT INTO goals (user_id, monthly_goal, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id)
            DO UPDATE SET monthly_goal = excluded.monthly_goal, updated_at = CURRENT_TIMESTAMP
            """,
            "",
            (user["id"], goal_value),
        )
    else:
        execute_write(
            "",
            """
            INSERT INTO goals (user_id, monthly_goal, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id)
            DO UPDATE SET monthly_goal = EXCLUDED.monthly_goal, updated_at = CURRENT_TIMESTAMP
            """,
            (user["id"], goal_value),
        )

    flash("Meta guardada com sucesso.", "success")
    return redirect(url_for("app_dashboard"))


@app.route("/feedback", methods=["POST"])
@login_required
def save_feedback():
    user = current_user()
    message = request.form.get("message", "").strip()

    if not message:
        flash("Escreve uma mensagem de feedback.", "error")
        return redirect(url_for("app_dashboard"))

    execute_write(
        "INSERT INTO feedback (user_id, message) VALUES (?, ?)",
        "INSERT INTO feedback (user_id, message) VALUES (%s, %s)",
        (user["id"], message),
    )

    flash("Feedback enviado com sucesso.", "success")
    return redirect(url_for("app_dashboard"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin_ok"] = True
            flash("Acesso admin concedido.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Senha admin inválida.", "error")

    return render_template_string(ADMIN_LOGIN_TEMPLATE)


@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_ok", None)
    flash("Sessão admin terminada.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    total_users_row = fetch_one(
        "SELECT COUNT(*) AS total FROM users",
        "SELECT COUNT(*) AS total FROM users",
        (),
    )
    total_movements_row = fetch_one(
        "SELECT COUNT(*) AS total FROM movements",
        "SELECT COUNT(*) AS total FROM movements",
        (),
    )
    total_feedback_row = fetch_one(
        "SELECT COUNT(*) AS total FROM feedback",
        "SELECT COUNT(*) AS total FROM feedback",
        (),
    )

    users = fetch_all(
        "SELECT * FROM users ORDER BY created_at DESC, id DESC LIMIT 100",
        "SELECT * FROM users ORDER BY created_at DESC, id DESC LIMIT 100",
        (),
    )

    feedbacks = fetch_all(
        """
        SELECT f.*, u.username
        FROM feedback f
        LEFT JOIN users u ON u.id = f.user_id
        ORDER BY f.created_at DESC, f.id DESC
        LIMIT 100
        """,
        """
        SELECT f.*, u.username
        FROM feedback f
        LEFT JOIN users u ON u.id = f.user_id
        ORDER BY f.created_at DESC, f.id DESC
        LIMIT 100
        """,
        (),
    )

    movements = fetch_all(
        """
        SELECT m.*, u.username
        FROM movements m
        JOIN users u ON u.id = m.user_id
        ORDER BY m.created_at DESC, m.id DESC
        LIMIT 100
        """,
        """
        SELECT m.*, u.username
        FROM movements m
        JOIN users u ON u.id = m.user_id
        ORDER BY m.created_at DESC, m.id DESC
        LIMIT 100
        """,
        (),
    )

    return render_template_string(
        ADMIN_TEMPLATE,
        total_users=total_users_row["total"],
        total_movements=total_movements_row["total"],
        total_feedback=total_feedback_row["total"],
        users=users,
        feedbacks=feedbacks,
        movements=movements,
    )


# =========================================================
# STARTUP
# =========================================================
init_db()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
