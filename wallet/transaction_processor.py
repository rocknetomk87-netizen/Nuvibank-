from wallet.validator import validate_balance
from wallet.ledger.engine import create_ledger_entry
from services.transaction_service import generate_transaction_id
from core.db import db


def process_transaction(
    sender_wallet,
    receiver_wallet,
    amount
):

    if not validate_balance(
        sender_wallet,
        amount
    ):

        return {
            "success": False,
            "message": "Insufficient balance"
        }

    transaction_id = generate_transaction_id()

    sender_before = sender_wallet.available_balance
    receiver_before = receiver_wallet.available_balance

    sender_wallet.available_balance -= amount
    receiver_wallet.available_balance += amount

    db.session.commit()

    create_ledger_entry(
        transaction_id,
        sender_wallet.user_id,
        "DEBIT",
        amount,
        sender_before,
        sender_wallet.available_balance,
        "Transfer sent"
    )

    create_ledger_entry(
        transaction_id,
        receiver_wallet.user_id,
        "CREDIT",
        amount,
        receiver_before,
        receiver_wallet.available_balance,
        "Transfer received"
    )

    return {
        "success": True,
        "transaction_id": transaction_id
    }
