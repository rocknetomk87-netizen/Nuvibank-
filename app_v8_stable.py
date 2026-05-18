from flask import Flask, request, jsonify
import jwt
import datetime
import bcrypt
import sqlite3
import logging

# =========================
# APP
# =========================

app = Flask(__name__)

# =========================
# CONFIG
# =========================

SECRET_KEY = (
    "NUVIBANK_V8_ULTRA_SECURE_"
    "BANKING_SYSTEM_2026_X9"
)

DB_NAME = "nuvibank.db"

# =========================
# LOGGER
# =========================

logging.basicConfig(
    filename="nuvibank.log",
    level=logging.INFO
)

# =========================
# DATABASE
# =========================

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
    balance REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    amount REAL,
    created_at TEXT
)
""")

conn.commit()

# =========================
# FRONTEND
# =========================

@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html>

<head>

<title>
NUVIBANK V8
</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

body{

    background:#041533;

    color:white;

    font-family:Arial;

    margin:0;

    padding:20px;
}

.logo{

    font-size:32px;

    font-weight:bold;

    margin-bottom:20px;
}

.card{

    background:#1b2d52;

    padding:25px;

    border-radius:20px;

    margin-bottom:20px;
}

input{

    width:100%;

    padding:18px;

    margin-top:15px;

    border:none;

    border-radius:14px;

    background:#3a4f74;

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

    background:#8a2eff;

    color:white;

    font-size:22px;

    font-weight:bold;

    cursor:pointer;
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

<div class="logo">
🏦 NUVIBANK V8
</div>

<div class="card">

<h2>
Servidor Online
</h2>

<p>
Frontend restaurado.
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

<button onclick="transferMoney()">
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

<div id="user_area" class="card">

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

    const username =
        document.getElementById(
            "register_username"
        ).value

    const password =
        document.getElementById(
            "register_password"
        ).value

    const response = await fetch(
        "/register",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                username:username,
                password:password
            })
        }
    )

    const data = await response.json()

    alert(
        data.message || data.error
    )
}

async function login(){

    const username =
        document.getElementById(
            "login_username"
        ).value

    const password =
        document.getElementById(
            "login_password"
        ).value

    const response = await fetch(
        "/login",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                username:username,
                password:password
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
    }

    alert(
        data.message || data.error
    )
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
    ).innerText = data.username

    document.getElementById(
        "balance"
    ).innerText =
        "Saldo: " +
        data.balance +
        " KZ"
}

async function transferMoney(){

    const receiver =
        document.getElementById(
            "receiver"
        ).value

    const amount =
        document.getElementById(
            "amount"
        ).value

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
                receiver:receiver,
                amount:amount
            })
        }
    )

    const data = await response.json()

    alert(
        data.message || data.error
    )

    loadUser()

    loadTransactions()
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

    document.getElementById(
        "history"
    ).innerHTML =
        html || "Sem transações"
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
    ).innerText =
        "Saldo: 0 KZ"

    document.getElementById(
        "history"
    ).innerHTML =
        "Sem transações"

    alert(
        "Logout realizado"
    )
}

window.onload = () => {

    if(TOKEN){

        loadUser()

        loadTransactions()
    }
}

</script>

</body>
</html>
"""

# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        username = data.get(
            "username"
        )

        password = data.get(
            "password"
        )

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

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

        return jsonify({
            "message":
            "Conta criada"
        })

    except Exception as e:

        logging.error(e)

        return jsonify({
            "error":
            "Erro ao criar conta"
        })

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login_api():

    try:

        data = request.get_json()

        username = data.get(
            "username"
        )

        password = data.get(
            "password"
        )

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
                "error":
                "Utilizador inválido"
            })

        if not bcrypt.checkpw(
            password.encode(),
            user[0]
        ):

            return jsonify({
                "error":
                "Password inválida"
            })

        token = jwt.encode(
            {
                "username":username,
                "exp":
                datetime.datetime.now(
                    datetime.UTC
                ) +
                datetime.timedelta(
                    days=1
                )
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "token":token
        })

    except Exception as e:

        logging.error(e)

        return jsonify({
            "error":
            "Erro login"
        })

# =========================
# TRANSFER
# =========================

@app.route("/transfer", methods=["POST"])
def transfer():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify({
                "error":
                "Token missing"
            })

        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        sender = decoded["username"]

        data = request.get_json()

        receiver = data.get(
            "receiver"
        )

        amount = float(
            data.get("amount")
        )

        if amount <= 0:

            return jsonify({
                "error":
                "Valor inválido"
            })

        if sender == receiver:

            return jsonify({
                "error":
                "Não podes transferir para ti"
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

            return jsonify({
                "error":
                "Sender not found"
            })

        sender_balance = sender_data[0]

        if sender_balance < amount:

            return jsonify({
                "error":
                "Saldo insuficiente"
            })

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username=?
            """,
            (receiver,)
        )

        receiver_exists = cursor.fetchone()

        if not receiver_exists:

            return jsonify({
                "error":
                "Destinatário não existe"
            })

        new_sender_balance = (
            sender_balance - amount
        )

        cursor.execute(
            """
            UPDATE users
            SET balance=?
            WHERE username=?
            """,
            (
                new_sender_balance,
                sender
            )
        )

        cursor.execute(
            """
            UPDATE users
            SET balance =
            balance + ?
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
                created_at
            )
            VALUES(?,?,?,?)
            """,
            (
                sender,
                receiver,
                amount,
                str(
                    datetime.datetime.now(
                        datetime.UTC
                    )
                )
            )
        )

        conn.commit()

        conn.close()

        return jsonify({
            "message":
            "Transferência realizada"
        })

    except Exception as e:

        logging.error(e)

        return jsonify({
            "error":
            "Transfer failed"
        })

# =========================
# HISTORY
# =========================

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

        transactions = []

        for row in data:

            transactions.append({
                "sender":row[0],
                "receiver":row[1],
                "amount":row[2],
                "created_at":row[3]
            })

        return jsonify(
            transactions
        )

    except Exception as e:

        logging.error(e)

        return jsonify([])

# =========================
# ME
# =========================

@app.route("/me")
def me():

    try:

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return jsonify({
                "error":
                "No token"
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
            SELECT balance
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        balance = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            "username":username,
            "balance":balance
        })

    except Exception as e:

        logging.error(e)

        return jsonify({
            "error":
            "Invalid token"
        })

# =========================
# RUN
# =========================

if __name__ == "__main__":

    print(
        "NUVIBANK SERVER STARTED"
    )

    app.run(
        host="0.0.0.0",
        port=5000
    )
