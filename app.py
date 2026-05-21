from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

import datetime
import os

app = Flask(__name__)

# CONFIG
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'nuvibank.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT SECRET PROFISSIONAL
app.config['JWT_SECRET_KEY'] = 'NUVIBANK_ULTRA_SECRET_KEY_2026_SECURE_SYSTEM'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)


# =========================
# MODELOS
# =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    balance = db.Column(db.Float, default=0)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender = db.Column(db.String(80))

    recipient = db.Column(db.String(80))

    amount = db.Column(db.Float)

    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC)
    )


# =========================
# CRIAR BASE
# =========================

with app.app_context():

    db.create_all()

    admin = User.query.filter_by(username='admin').first()

    if not admin:

        hashed = bcrypt.generate_password_hash(
            'admin123'
        ).decode('utf-8')

        admin_user = User(
            username='admin',
            password=hashed,
            balance=100000
        )

        db.session.add(admin_user)
        db.session.commit()

        print("✅ ADMIN CRIADO")


# =========================
# LOGIN
# =========================

@app.route('/login', methods=['POST'])
def login():

    data = request.json

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({
            "error": "Utilizador não encontrado"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "error": "Senha inválida"
        }), 401

    token = create_access_token(
        identity=username,
        expires_delta=datetime.timedelta(hours=24)
    )

    return jsonify({
        "token": token,
        "user": username
    })


# =========================
# BALANCE
# =========================

@app.route('/balance/<username>', methods=['GET'])
def balance(username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({
            "error": "Utilizador não encontrado"
        }), 404

    return jsonify({
        "balance": user.balance
    })


# =========================
# TRANSFER
# =========================

@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():

    data = request.json

    sender = get_jwt_identity()

    recipient = data.get('recipient')

    amount = float(data.get('amount'))

    sender_user = User.query.filter_by(username=sender).first()

    recipient_user = User.query.filter_by(
        username=recipient
    ).first()

    if not recipient_user:

        return jsonify({
            "error": "Destinatário não encontrado"
        }), 404

    if amount <= 0:

        return jsonify({
            "error": "Valor inválido"
        }), 400

    if sender_user.balance < amount:

        return jsonify({
            "error": "Saldo insuficiente"
        }), 400

    sender_user.balance -= amount

    recipient_user.balance += amount

    transaction = Transaction(
        sender=sender,
        recipient=recipient,
        amount=amount
    )

    db.session.add(transaction)

    db.session.commit()

    return jsonify({
        "message": "Transferência realizada"
    })


# =========================
# HISTÓRICO
# =========================

@app.route('/transactions', methods=['GET'])
def transactions():

    all_transactions = Transaction.query.order_by(
        Transaction.id.desc()
    ).all()

    result = []

    for tx in all_transactions:

        result.append({
            "sender": tx.sender,
            "recipient": tx.recipient,
            "amount": tx.amount,
            "created_at": str(tx.created_at)
        })

    return jsonify(result)


# =========================
# CRIAR UTILIZADOR
# =========================

@app.route('/create-user', methods=['POST'])
def create_user():

    data = request.json

    username = data.get('username')
    password = data.get('password')

    exists = User.query.filter_by(
        username=username
    ).first()

    if exists:

        return jsonify({
            "error": "Utilizador já existe"
        }), 400

    hashed = bcrypt.generate_password_hash(
        password
    ).decode('utf-8')

    user = User(
        username=username,
        password=hashed,
        balance=0
    )

    db.session.add(user)

    db.session.commit()

    return jsonify({
        "message": "Utilizador criado"
    })


# =========================
# SERVER
# =========================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
