from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET = "SUPER_SECRET_KEY"

# "Banco" fake (memória)
users = {}
balances = {}

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    password = data["password"]

    if name in users:
        return jsonify({"error": "User exists"})

    users[name] = password
    balances[name] = 0

    return jsonify({"message": "User created"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data["name"]
    password = data["password"]

    if name not in users or users[name] != password:
        return jsonify({"error": "Invalid credentials"})

    token = jwt.encode({
        "name": name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET, algorithm="HS256")

    return jsonify({"message": "Login OK", "token": token})

# ---------------- AUTH ----------------
def verify_token(req):
    auth = req.headers.get("Authorization")
    if not auth:
        return None

    try:
        token = auth.split(" ")[1]
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["name"]
    except:
        return None

# ---------------- ME ----------------
@app.route("/me", methods=["GET"])
def me():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"})

    return jsonify({
        "name": user,
        "balance": balances[user]
    })

# ---------------- DEPOSIT ----------------
@app.route("/deposit", methods=["POST"])
def deposit():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"})

    value = float(request.json["valor"])
    balances[user] += value

    return jsonify({"message": "Deposit OK", "balance": balances[user]})

# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["POST"])
def transfer():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"})

    to = request.json["to_id"]
    value = float(request.json["valor"])

    if to not in balances:
        return jsonify({"error": "User not found"})

    if balances[user] < value:
        return jsonify({"error": "Insufficient funds"})

    balances[user] -= value
    balances[to] += value

    return jsonify({"message": "Transfer OK", "balance": balances[user]})

# ---------------- FRONTEND ----------------
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>NUVIBANK V6</title>
</head>
<body>

<h1>NUVIBANK V6 🔐</h1>

<h2>Login</h2>
<input id="loginName" placeholder="Nome">
<input id="loginPass" type="password" placeholder="Password">
<button onclick="login()">Login</button>

<h2>Criar conta</h2>
<input id="regName" placeholder="Nome">
<input id="regPass" type="password" placeholder="Password">
<button onclick="register()">Criar</button>

<h2>Dashboard</h2>
<p id="userInfo">Não logado</p>
<button onclick="me()">Atualizar sessão</button>
<button onclick="logout()">Logout</button>

<h2>Depositar</h2>
<input id="depositValue" placeholder="Valor">
<button onclick="deposit()">Depositar</button>

<h2>Transferir</h2>
<input id="toId" placeholder="Nome destino">
<input id="transferValue" placeholder="Valor">
<button onclick="transfer()">Transferir</button>

<script>

async function login() {
    const name = document.getElementById("loginName").value;
    const password = document.getElementById("loginPass").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, password})
    });

    const data = await res.json();

    if (data.token) {
        localStorage.setItem("token", data.token);
        alert("Login OK");
    } else {
        alert("Erro login");
    }
}

async function register() {
    const name = document.getElementById("regName").value;
    const password = document.getElementById("regPass").value;

    const res = await fetch("/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, password})
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}

async function me() {
    const token = localStorage.getItem("token");

    const res = await fetch("/me", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await res.json();

    document.getElementById("userInfo").innerText =
        "Nome: " + data.name + " | Saldo: " + data.balance;
}

function logout() {
    localStorage.removeItem("token");
    alert("Logout feito");
}

async function deposit() {
    const token = localStorage.getItem("token");
    const valor = document.getElementById("depositValue").value;

    const res = await fetch("/deposit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({valor})
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}

async function transfer() {
    const token = localStorage.getItem("token");
    const to_id = document.getElementById("toId").value;
    const valor = document.getElementById("transferValue").value;

    const res = await fetch("/transfer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({to_id, valor})
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}

</script>

</body>
</html>
"""

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
