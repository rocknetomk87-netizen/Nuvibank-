from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Base temporária em memória
users = {}
next_id = 1


def find_user_by_name(name: str):
    for user in users.values():
        if user["name"].lower() == name.lower():
            return user
    return None


@app.route("/")
def home():
    return jsonify({
        "app": "NUVIBANK",
        "status": "online",
        "version": "v3"
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/test")
def api_test():
    return jsonify({"message": "API NUVIBANK v3 funcionando"})


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify({
        "total": len(users),
        "users": list(users.values())
    })


@app.route("/users", methods=["POST"])
def create_user():
    global next_id

    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({"error": "Nome é obrigatório"}), 400

    if find_user_by_name(name):
        return jsonify({"error": "Utilizador já existe"}), 409

    user = {
        "id": next_id,
        "name": name,
        "balance": 0.0
    }
    users[next_id] = user
    next_id += 1

    return jsonify({
        "message": "Utilizador criado com sucesso",
        "user": user
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    if not name:
        return jsonify({"error": "Nome é obrigatório"}), 400

    user = find_user_by_name(name)
    if not user:
        return jsonify({"error": "Utilizador não encontrado"}), 404

    return jsonify({
        "message": "Login simulado com sucesso",
        "user": user
    })


@app.route("/balance/<int:user_id>", methods=["GET"])
def get_balance(user_id: int):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "Utilizador não encontrado"}), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"],
        "balance": user["balance"]
    })


@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    amount = data.get("amount")

    if user_id is None or amount is None:
        return jsonify({"error": "user_id e amount são obrigatórios"}), 400

    try:
        user_id = int(user_id)
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "user_id ou amount inválido"}), 400

    if amount <= 0:
        return jsonify({"error": "O valor deve ser maior que zero"}), 400

    user = users.get(user_id)
    if not user:
        return jsonify({"error": "Utilizador não encontrado"}), 404

    user["balance"] += amount

    return jsonify({
        "message": "Depósito realizado com sucesso",
        "user": user
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json(silent=True) or {}

    from_user_id = data.get("from_user_id")
    to_user_id = data.get("to_user_id")
    amount = data.get("amount")

    if from_user_id is None or to_user_id is None or amount is None:
        return jsonify({
            "error": "from_user_id, to_user_id e amount são obrigatórios"
        }), 400

    try:
        from_user_id = int(from_user_id)
        to_user_id = int(to_user_id)
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Dados inválidos"}), 400

    if amount <= 0:
        return jsonify({"error": "O valor deve ser maior que zero"}), 400

    if from_user_id == to_user_id:
        return jsonify({"error": "Não pode transferir para a mesma conta"}), 400

    sender = users.get(from_user_id)
    receiver = users.get(to_user_id)

    if not sender:
        return jsonify({"error": "Remetente não encontrado"}), 404

    if not receiver:
        return jsonify({"error": "Destinatário não encontrado"}), 404

    if sender["balance"] < amount:
        return jsonify({"error": "Saldo insuficiente"}), 400

    sender["balance"] -= amount
    receiver["balance"] += amount

    return jsonify({
        "message": "Transferência realizada com sucesso",
        "from": sender,
        "to": receiver,
        "amount": amount
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
