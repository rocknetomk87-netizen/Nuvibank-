from core_bank.core_app import app

from core_bank.database.db_engine import db

from core_bank.banking.users.user_model import User

from core_bank.banking.wallets.wallet_model import Wallet

from core_bank.ledger_engine.transactions.transaction_processor import transfer


with app.app_context():

    user1 = User(
        username="ceo",
        email="ceo@nuvibank.com",
        password="123"
    )

    user2 = User(
        username="client",
        email="client@nuvibank.com",
        password="123"
    )

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    wallet1 = Wallet(
        user_id=user1.id,
        balance=1000
    )

    wallet2 = Wallet(
        user_id=user2.id,
        balance=100
    )

    db.session.add(wallet1)
    db.session.add(wallet2)

    db.session.commit()

    result = transfer(
        wallet1.id,
        wallet2.id,
        250
    )

    print(result)

    print("Wallet Sender:", wallet1.balance)

    print("Wallet Receiver:", wallet2.balance)
