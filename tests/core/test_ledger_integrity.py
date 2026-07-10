from decimal import Decimal

from core_bank.models.user import User
from core_bank.models.account import Account
from core_bank.ledger.models.ledger_entry import LedgerEntry
from core_bank.finance.core.transaction_service import TransactionService
from core_bank.extensions import db


def test_ledger_integrity_after_transfer(app):

    with app.app_context():

        # Criar utilizadores

        sender = User(
            username="ledger_sender",
            email="ledger_sender@nuvibank.com",
            password="hash"
        )

        receiver = User(
            username="ledger_receiver",
            email="ledger_receiver@nuvibank.com",
            password="hash"
        )


        db.session.add(sender)
        db.session.add(receiver)

        db.session.flush()


        # Criar contas

        sender_account = Account(
            user_id=sender.id,
            balance=Decimal("5000.00"),
            currency="AOA"
        )

        receiver_account = Account(
            user_id=receiver.id,
            balance=Decimal("1000.00"),
            currency="AOA"
        )


        db.session.add(sender_account)
        db.session.add(receiver_account)

        db.session.commit()


        # Executar transferência

        transaction = TransactionService.transfer(
            sender_account.id,
            receiver_account.id,
            Decimal("1500.00")
        )


        # Buscar lançamentos

        entries = LedgerEntry.query.filter_by(
            transaction_id=transaction.id
        ).all()


        # Deve existir débito e crédito

        assert len(entries) == 2


        debit = next(
            entry for entry in entries
            if entry.entry_type == "DEBIT"
        )

        credit = next(
            entry for entry in entries
            if entry.entry_type == "CREDIT"
        )


        # Validar valores

        assert debit.amount == Decimal("1500.00")
        assert credit.amount == Decimal("1500.00")


        # Validar contas

        assert debit.account_id == sender_account.id
        assert credit.account_id == receiver_account.id


        # Validar conservação financeira

        assert debit.amount == credit.amount
