from flask import Blueprint, request, jsonify

from core_bank.core_app import db
from core_bank.models.account import Account
from core_bank.models.transaction import Transaction


transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json() or {}

    account_number = data.get("account_number")
    amount = data.get("amount")

    if not account_number or amount is None:
        return jsonify({"error": "Missing data"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    account = Account.query.filter_by(account_number=account_number).first()

    if not account:
        return jsonify({"error": "Account not found"}), 404

    account.balance += amount

    transaction = Transaction(
        sender_account=account.account_number,
        receiver_account=account.account_number,
        amount=amount,
        transaction_type="DEPOSIT",
        status="SUCCESS",
        description="Account deposit"
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Deposit successful",
        "account_number": account.account_number,
        "new_balance": account.balance
    }), 200


@transactions_bp.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json() or {}

    sender_account_number = data.get("sender_account")
    receiver_account_number = data.get("receiver_account")
    amount = data.get("amount")

    if not sender_account_number or not receiver_account_number or amount is None:
        return jsonify({"error": "Missing data"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    if sender_account_number == receiver_account_number:
        return jsonify({"error": "Cannot transfer to same account"}), 400

    sender = Account.query.filter_by(account_number=sender_account_number).first()
    receiver = Account.query.filter_by(account_number=receiver_account_number).first()

    if not sender:
        return jsonify({"error": "Sender account not found"}), 404

    if not receiver:
        return jsonify({"error": "Receiver account not found"}), 404

    if sender.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    sender.balance -= amount
    receiver.balance += amount

    transaction = Transaction(
        sender_account=sender.account_number,
        receiver_account=receiver.account_number,
        amount=amount,
        transaction_type="TRANSFER",
        status="SUCCESS",
        description="Internal transfer"
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transfer successful",
        "sender_balance": sender.balance,
        "receiver_balance": receiver.balance
    }), 200


@transactions_bp.route("/transactions", methods=["GET"])
def list_transactions():
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()

    return jsonify({
        "total": len(transactions),
        "transactions": [t.to_dict() for t in transactions]
    }), 200


@transactions_bp.route("/account/<account_number>/statement", methods=["GET"])
def account_statement(account_number):
    account = Account.query.filter_by(account_number=account_number).first()

    if not account:
        return jsonify({"error": "Account not found"}), 404

    transactions = Transaction.query.filter(
        (Transaction.sender_account == account_number) |
        (Transaction.receiver_account == account_number)
    ).order_by(Transaction.id.desc()).all()

    return jsonify({
        "account_number": account.account_number,
        "balance": account.balance,
        "currency": account.currency,
        "status": account.status,
        "total_transactions": len(transactions),
        "transactions": [t.to_dict() for t in transactions]
    }), 200
