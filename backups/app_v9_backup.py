from flask import Flask, request, jsonify
import jwt
import datetime
import bcrypt
import sqlite3
import logging

# ==========================================
# APP
# ==========================================

app = Flask(__name__)

DB_NAME = "nuvibank.db"

SECRET_KEY = (
    "NUVIBANK_V8_ULTRA_SECURE_"
    "BANKING_SYSTEM_2026_X9"
)

logging.basicConfig(
    filename="nuvibank.log",
    level=logging.INFO
)

# ==========================================
# DATABASE
# ==========================================

conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    balance REAL DEFAULT 0,

    role TEXT DEFAULT 'user'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sender TEXT,

    receiver TEXT,

    amount REAL,

    type TEXT,

    created_at TEXT
)
""")

conn.commit()

# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.json

        username = data["username"].strip()

        password = data["password"]

        if not username or not password:

            return jsonify({
                "error": "Dados inválidos"
            })

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(
                username,
                password
            )
            VALUES(?,?)
            """,
            (
                username,
                hashed
            )
        )

        conn.commit()

        conn.close()

        logging.info(
            f"NEW USER: {username}"
        )

        return jsonify({
            "message": "Conta criada"
        })

    except Exception as e:

        logging.error(
            f"REGISTER ERROR: {e}"
        )

        return jsonify({
            "error": "Erro ao criar conta"
        })

# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.json

        username = data["username"]

        password = data["password"]

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if not user:

            return jsonify({
                "error": "Conta não encontrada"
            })

        stored_password = user[0]

        if not bcrypt.checkpw(
            password.encode(),
            stored_password.encode()
        ):

            return jsonify({
                "error": "Password inválida"
            })

        token = jwt.encode(
            {
                "username": username,
                "exp": (
                    datetime.datetime.utcnow()
                    + datetime.timedelta(days=1)
                )
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        logging.info(
            f"LOGIN: {username}"
        )

        return jsonify({
            "token": token
        })

    except Exception as e:

        logging.error(
            f"LOGIN ERROR: {e}"
        )

        return jsonify({
            "error": "Erro no login"
        })

# ==========================================
# TRANSFER
# ==========================================

@app.route("/transfer", methods=["POST"])
def transfer():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify({
                "error": "Token missing"
            })

        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        sender = decoded["username"]

        data = request.json

        receiver = data["receiver"]

        amount = float(data["amount"])

        if amount <= 0:

            return jsonify({
                "error": "Valor inválido"
            })

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE username=?
            """,
            (sender,)
        )

        sender_data = cursor.fetchone()

        if not sender_data:

            conn.close()

            return jsonify({
                "error": "Remetente inválido"
            })

        sender_balance = sender_data[0]

        if sender_balance < amount:

            conn.close()

            return jsonify({
                "error": "Saldo insuficiente"
            })

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE username=?
            """,
            (receiver,)
        )

        receiver_data = cursor.fetchone()

        if not receiver_data:

            conn.close()

            return jsonify({
                "error": "Destinatário inválido"
            })

        cursor.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE username=?
            """,
            (
                amount,
                sender
            )
        )

        cursor.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE username=?
            """,
            (
                amount,
                receiver
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions(
                sender,
                receiver,
                amount,
                type,
                created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                sender,
                receiver,
                amount,
                "transfer",
                str(
                    datetime.datetime.utcnow()
                )
            )
        )

        conn.commit()

        conn.close()

        logging.info(
            f"TRANSFER: {sender} -> {receiver} : {amount}"
        )

        return jsonify({
            "message": "Transferência realizada"
        })

    except Exception as e:

        logging.error(
            f"TRANSFER ERROR: {e}"
        )

        return jsonify({
            "error": "Erro na transferência"
        })

# ==========================================
# TRANSACTIONS
# ==========================================

@app.route("/transactions", methods=["GET"])
def transactions():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify([])

        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = decoded["username"]

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                sender,
                receiver,
                amount,
                created_at
            FROM transactions
            WHERE sender=?
            OR receiver=?
            ORDER BY id DESC
            LIMIT 10
            """,
            (
                username,
                username
            )
        )

        data = cursor.fetchall()

        conn.close()

        transactions_data = []

        for row in data:

            transactions_data.append({

                "sender": row[0],

                "receiver": row[1],

                "amount": row[2],

                "created_at": row[3]
            })

        return jsonify(
            transactions_data
        )

    except Exception as e:

        logging.error(
            f"TRANSACTIONS ERROR: {e}"
        )

        return jsonify([])

# ==========================================
# ADMIN
# ==========================================

@app.route("/admin", methods=["GET"])
def admin_panel():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify({
                "error": "Token missing"
            })

        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = decoded["username"]

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        role_data = cursor.fetchone()

        if not role_data:

            conn.close()

            return jsonify({
                "error": "User not found"
            })

        if role_data[0] != "admin":

            conn.close()

            return jsonify({
                "error": "Access denied"
            })

        cursor.execute(
            """
            SELECT
                username,
                balance,
                role
            FROM users
            """
        )

        users = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                sender,
                receiver,
                amount,
                created_at
            FROM transactions
            ORDER BY id DESC
            LIMIT 20
            """
        )

        transactions = cursor.fetchall()

        cursor.execute(
            """
            SELECT SUM(balance)
            FROM users
            """
        )

        total_balance = cursor.fetchone()[0]

        conn.close()

        users_data = []

        for user in users:

            users_data.append({

                "username": user[0],

                "balance": user[1],

                "role": user[2]
            })

        tx_data = []

        for tx in transactions:

            tx_data.append({

                "sender": tx[0],

                "receiver": tx[1],

                "amount": tx[2],

                "created_at": tx[3]
            })

        return jsonify({

            "bank_balance": total_balance,

            "users": users_data,

            "transactions": tx_data
        })

    except Exception as e:

        logging.error(
            f"ADMIN ERROR: {e}"
        )

        return jsonify({
            "error": "Admin failed"
        })

# ==========================================
# ME
# ==========================================

@app.route("/me", methods=["GET"])
def me():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify({
                "error": "Token missing"
            })

        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = decoded["username"]

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                username,
                balance,
                role
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if not user:

            return jsonify({
                "error": "User not found"
            })

        return jsonify({

            "username": user[0],

            "balance": user[1],

            "role": user[2]
        })

    except Exception as e:

        logging.error(
            f"ME ERROR: {e}"
        )

        return jsonify({
            "error": "Erro ao carregar conta"
        })

# ==========================================
# FRONTEND
# ==========================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html>

<head>

<title>
NUVIBANK V9
</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

body{

    background:#071739;

    color:white;

    font-family:Arial;

    padding:20px;
}

.card{

    background:#1f2f5a;

    padding:20px;

    margin-top:20px;

    border-radius:20px;
}

input{

    width:100%;

    padding:18px;

    margin-top:10px;

    border:none;

    border-radius:14px;

    background:#405886;

    color:white;

    font-size:18px;

    box-sizing:border-box;
}

button{

    width:100%;

    padding:18px;

    margin-top:15px;

    border:none;

    border-radius:14px;

    background:#9b35ff;

    color:white;

    font-size:22px;

    font-weight:bold;
}

.tx{

    background:#263859;

    padding:15px;

    margin-top:10px;

    border-radius:12px;
}

</style>

</head>

<body>

<h1>
🏦 NUVIBANK V9
</h1>

<div class="card">

<h2>
Servidor Online
</h2>

<p>
Sistema bancário operacional.
</p>

</div>

<div class="card">

<h2>
Login
</h2>

<input
id="login_username"
placeholder="Nome">

<input
id="login_password"
type="password"
placeholder="Password">

<button onclick="login()">
Entrar
</button>

</div>

<div class="card">

<h2>
Criar Conta
</h2>

<input
id="register_username"
placeholder="Nome">

<input
id="register_password"
type="password"
placeholder="Password">

<button onclick="register()">
Criar Conta
</button>

</div>

<div class="card">

<h2>
Transferir
</h2>

<input
id="receiver"
placeholder="Destinatário">

<input
id="amount"
placeholder="Valor">

<button onclick="transfer()">
Transferir
</button>

</div>

<div class="card">

<h2>
Histórico
</h2>

<div id="history">
Sem transações
</div>

</div>

<div class="card">

<h2>
Painel Admin
</h2>

<div id="admin_panel">

Banco: 0 KZ

<br><br>

Sem dados

</div>

</div>

<div
class="card"
id="user_area">

<h2>
Conta
</h2>

<p id="username">
...
</p>

<p id="balance">
Saldo: 0 KZ
</p>

<button onclick="logout()">
Logout
</button>

</div>

<script>

let TOKEN = localStorage.getItem(
    "token"
) || ""

async function register(){

    const response = await fetch(
        "/register",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                username:
                document.getElementById(
                    "register_username"
                ).value,

                password:
                document.getElementById(
                    "register_password"
                ).value
            })
        }
    )

    const data = await response.json()

    alert(
        data.message || data.error
    )
}

async function login(){

    const response = await fetch(
        "/login",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                username:
                document.getElementById(
                    "login_username"
                ).value,

                password:
                document.getElementById(
                    "login_password"
                ).value
            })
        }
    )

    const data = await response.json()

    if(data.token){

        TOKEN = data.token

        localStorage.setItem(
            "token",
            TOKEN
        )

        loadUser()

        loadTransactions()

        loadAdmin()

        alert("Login realizado")

    }else{

        alert(
            data.error
        )
    }
}

async function transfer(){

    const response = await fetch(
        "/transfer",
        {
            method:"POST",

            headers:{

                "Content-Type":
                "application/json",

                "Authorization":
                "Bearer " + TOKEN
            },

            body:JSON.stringify({

                receiver:
                document.getElementById(
                    "receiver"
                ).value,

                amount:
                document.getElementById(
                    "amount"
                ).value
            })
        }
    )

    const data = await response.json()

    alert(
        data.message || data.error
    )

    loadUser()

    loadTransactions()

    loadAdmin()
}

async function loadUser(){

    if(!TOKEN){
        return
    }

    const response = await fetch(
        "/me",
        {
            headers:{
                "Authorization":
                "Bearer " + TOKEN
            }
        }
    )

    const data = await response.json()

    document.getElementById(
        "username"
    ).innerText =
    data.username || "Utilizador"

    document.getElementById(
        "balance"
    ).innerText =
    "Saldo: " +
    (
        data.balance || 0
    ) +
    " KZ"
}

async function loadTransactions(){

    if(!TOKEN){
        return
    }

    const response = await fetch(
        "/transactions",
        {
            headers:{
                "Authorization":
                "Bearer " + TOKEN
            }
        }
    )

    const data = await response.json()

    let html = ""

    for(const tx of data){

        html += `

        <div class="tx">

        <p>
        ${tx.sender}
        →
        ${tx.receiver}
        </p>

        <p>
        ${tx.amount} KZ
        </p>

        <p>
        ${tx.created_at}
        </p>

        </div>
        `
    }

    if(html === ""){

        html = "Sem transações"
    }

    document.getElementById(
        "history"
    ).innerHTML = html
}

async function loadAdmin(){

    if(!TOKEN){
        return
    }

    const response = await fetch(
        "/admin",
        {
            headers:{
                "Authorization":
                "Bearer " + TOKEN
            }
        }
    )

    const data = await response.json()

    if(data.error){
        return
    }

    let html = ""

    for(const user of data.users){

        html += `

        <div class="tx">

        <p>
        ${user.username}
        </p>

        <p>
        ${user.balance} KZ
        </p>

        <p>
        ${user.role}
        </p>

        </div>
        `
    }

    document.getElementById(
        "admin_panel"
    ).innerHTML = `

    <p>
    Banco:
    ${data.bank_balance} KZ
    </p>

    ${html}
    `
}

function logout(){

    TOKEN = ""

    localStorage.removeItem(
        "token"
    )

    document.getElementById(
        "username"
    ).innerText = "..."

    document.getElementById(
        "balance"
    ).innerText = "Saldo: 0 KZ"

    document.getElementById(
        "history"
    ).innerHTML = "Sem transações"

    alert(
        "Logout realizado"
    )
}

window.onload = () => {

    if(TOKEN){

        loadUser()

        loadTransactions()

        loadAdmin()
    }
}

</script>

</body>
</html>
"""

# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    print(
        "NUVIBANK V9 STARTED"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
