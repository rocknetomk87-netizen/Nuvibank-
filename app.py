from flask import Flask, jsonify, request
import os

app = Flask(__name__)


# Base temporária em memória.
# Limitação honesta: ao reiniciar o serviço, os dados desaparecem.
users = []
next_user_id = 1


def find_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_user_by_name(name: str):
    name = name.strip().lower()
    for user in users:
        if user["name"].strip().lower() == name:
            return user
    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "NUVIBANK",
        "status": "online",
        "version": "v4.1"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/test", methods=["GET"])
def api_test():
    return jsonify({
        "message": "API NUVIBANK funcionando"
    })


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({
        "total": len(users),
        "users": users
    })


@app.route("/users", methods=["POST"])
def create_user():
    global next_user_id

    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({
            "error": "O campo 'name' é obrigatório."
        }), 400

    if len(name) < 2:
        return jsonify({
            "error": "O nome deve ter pelo menos 2 caracteres."
        }), 400

    existing_user = find_user_by_name(name)
    if existing_user is not None:
        return jsonify({
            "error": "Já existe um utilizador com esse nome."
        }), 409

    user = {
        "id": next_user_id,
        "name": name,
        "balance": 0.0
    }

    users.append(user)
    next_user_id += 1

    return jsonify({
        "message": "Utilizador criado com sucesso.",
        "user": user
    }), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "Utilizador não encontrado."
        }), 404

    return jsonify(user)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({
            "error": "O campo 'name' é obrigatório."
        }), 400

    user = find_user_by_name(name)
    if user is None:
        return jsonify({
            "error": "Utilizador não encontrado."
        }), 404

    return jsonify({
        "message": "Login simulado com sucesso.",
        "user": user
    })


@app.route("/balance/<int:user_id>", methods=["GET"])
def get_balance(user_id: int):
    user = find_user_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "Utilizador não encontrado."
        }), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"],
        "balance": user["balance"]
    })


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
        return jsonify({
            "error": "O valor do depósito deve ser maior que zero."
        }), 400

    user = find_user_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "Utilizador não encontrado."
        }), 404

    user["balance"] += amount

    return jsonify({
        "message": "Depósito realizado com sucesso.",
        "user": user
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json(silent=True) or {}

    required_fields = ["from_user_id", "to_user_id", "amount"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"O campo '{field}' é obrigatório."
            }), 400

    try:
        from_user_id = int(data["from_user_id"])
        to_user_id = int(data["to_user_id"])
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Os dados enviados são inválidos."
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "O valor da transferência deve ser maior que zero."
        }), 400

    if from_user_id == to_user_id:
        return jsonify({
            "error": "Não é permitido transferir para a mesma conta."
        }), 400

    sender = find_user_by_id(from_user_id)
    receiver = find_user_by_id(to_user_id)

    if sender is None:
        return jsonify({
            "error": "Utilizador de origem não encontrado."
        }), 404

    if receiver is None:
        return jsonify({
            "error": "Utilizador de destino não encontrado."
        }), 404

    if sender["balance"] < amount:
        return jsonify({
            "error": "Saldo insuficiente."
        }), 400

    sender["balance"] -= amount
    receiver["balance"] += amount

    return jsonify({
        "message": "Transferência realizada com sucesso.",
        "from_user": sender,
        "to_user": receiver,
        "amount": amount
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
