from core_bank.database.db_engine import db

from core_bank.banking.wallets.wallet_model import Wallet
from core_bank.ledger_engine.transactions.transaction_model import Transaction


def process_transaction(
    sender_wallet_id,
    receiver_wallet_id,
    amount
):

    sender_wallet = Wallet.query.get(sender_wallet_id)
    receiver_wallet = Wallet.query.get(receiver_wallet_id)

    if not sender_wallet:

        return {
            "status": "error",
            "message": "sender_wallet_not_found"
        }

    if not receiver_wallet:

        return {
            "status": "error",
            "message": "receiver_wallet_not_found"
        }

    if amount <= 0:

        return {
            "status": "error",
            "message": "invalid_amount"
        }

    if sender_wallet.balance < amount:

        return {
            "status": "error",
            "message": "insufficient_balance"
        }

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    transaction = Transaction(
        sender_wallet_id=sender_wallet_id,
        receiver_wallet_id=receiver_wallet_id,
        amount=amount
    )

    db.session.add(transaction)

    db.session.commit()

    return {
        "status": "success",
        "transaction_id": transaction.id,
        "sender_balance": sender_wallet.balance,
        "receiver_balance": receiver_wallet.balance
    }
