from flask import request, jsonify

from core_bank.core_app import db

from core_bank.banking.users.user_model import User
from core_bank.banking.wallets.wallet_model import Wallet

from core_bank.security.auth_engine import AuthEngine

from core_bank.ledger.journal.journal_entry import JournalEntry


def register_routes(app):

    @app.route("/")
    def home():

        return jsonify({
            "status": "NUVIBANK CORE ONLINE"
        })

    @app.route("/create_user", methods=["POST"])
    def create_user():

        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:

            return jsonify({
                "status": "error",
                "message": "user_already_exists"
            }), 400

        hashed_password = AuthEngine.hash_password(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        wallet = Wallet(
            user_id=user.id,
            balance=1000.0
        )

        db.session.add(wallet)
        db.session.commit()

        token = AuthEngine.generate_token(
            user.id,
            user.username
        )

        return jsonify({
            "status": "user_created",
            "user_id": user.id,
            "wallet_id": wallet.id,
            "username": user.username,
            "email": user.email,
            "balance": wallet.balance,
            "token": token
        })

    @app.route("/login", methods=["POST"])
    def login():

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return jsonify({
                "status": "error",
                "message": "invalid_credentials"
            }), 401

        valid_password = AuthEngine.verify_password(
            password,
            user.password
        )

        if not valid_password:

            return jsonify({
                "status": "error",
                "message": "invalid_credentials"
            }), 401

        token = AuthEngine.generate_token(
            user.id,
            user.username
        )

        return jsonify({
            "status": "success",
            "token": token,
            "user": user.to_dict()
        })

    @app.route("/journal")
    def journal():

        entries = JournalEntry.query.all()

        result = []

        for entry in entries:

            result.append({
                "id": entry.id,
                "transaction_id": entry.transaction_id,
                "account_id": entry.account_id,
                "account_type": entry.account_type,
                "entry_type": entry.entry_type,
                "amount": entry.amount,
                "currency": entry.currency,
                "description": entry.description,
                "created_at": str(entry.created_at)
            })

        return jsonify(result)
