from decimal import Decimal

from core_bank.models.user import User
from core_bank.models.account import Account
from core_bank.ledger.models.ledger_entry import LedgerEntry
from core_bank.ledger.models.journal import Journal
from core_bank.finance.core.transaction_service import TransactionService
from core_bank.extensions import db


def test_account_transfer(app):

    with app.app_context():

        # Criar utilizadores

        sender = User(
            username="sender",
            email="sender@nuvibank.com",
            password="hash"
        )

        receiver = User(
            username="receiver",
            email="receiver@nuvibank.com",
            password="hash"
        )


        db.session.add(sender)
        db.session.add(receiver)

        db.session.flush()


        # Criar contas

        sender_account = Account(
            user_id=sender.id,
            balance=Decimal("1000.00"),
            currency="AOA"
        )


        receiver_account = Account(
            user_id=receiver.id,
            balance=Decimal("500.00"),
            currency="AOA"
        )


        db.session.add(sender_account)
        db.session.add(receiver_account)

        db.session.commit()


        # Executar transferência

        transaction = TransactionService.transfer(
            sender_account.id,
            receiver_account.id,
            Decimal("200.00"),
            currency="AOA"
        )


        # Validar Transaction

        assert transaction.id is not None
        assert transaction.amount == Decimal("200.00")
        assert transaction.status == "SUCCESS"


        # Atualizar objetos do banco

        db.session.refresh(sender_account)
        db.session.refresh(receiver_account)


        # Validar saldos

        assert sender_account.balance == Decimal("800.00")
        assert receiver_account.balance == Decimal("700.00")


        # Validar Ledger duplo

        entries = LedgerEntry.query.filter_by(
            transaction_id=transaction.id
        ).all()


        assert len(entries) == 2


        debit = next(
            e for e in entries
            if e.entry_type == "DEBIT"
        )

        credit = next(
            e for e in entries
            if e.entry_type == "CREDIT"
        )


        assert debit.amount == Decimal("200.00")
        assert credit.amount == Decimal("200.00")


        # Validar Journal

        journal = Journal.query.filter_by(
            reference=f"TX-{transaction.id}"
        ).first()


        assert journal is not None
        assert journal.transaction_type == "TRANSFER"
        assert journal.status == "POSTED"
