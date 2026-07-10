from decimal import Decimal, InvalidOperation

from core_bank.extensions import db

from core_bank.models.account import Account
from core_bank.models.transaction import Transaction
from core_bank.models.transaction_request import TransactionRequest

from core_bank.ledger.models.ledger_entry import LedgerEntry
from core_bank.ledger.models.journal import Journal

from core_bank.finance.audit.audit_trail import AuditTrail


class TransactionService:
    """
    NUVIBANK Transaction Engine V5

    Responsável por:
    - Transferências financeiras
    - Idempotência
    - Ledger contábil
    - Journal
    - Auditoria
    """

    @staticmethod
    def transfer(
        sender_account_id,
        receiver_account_id,
        amount,
        currency="AOA",
        request_id=None,
        username="SYSTEM"
    ):

        try:

            # ===============================
            # IDEMPOTENCY CHECK
            # ===============================

            if request_id:

                existing_request = (
                    TransactionRequest.query
                    .filter_by(
                        request_id=request_id
                    )
                    .first()
                )

                if existing_request:

                    return (
                        Transaction.query.get(
                            existing_request.transaction_id
                        )
                    )


            # ===============================
            # LOAD ACCOUNTS
            # ===============================

            sender = db.session.get(
                Account,
                sender_account_id
            )

            receiver = db.session.get(
                Account,
                receiver_account_id
            )


            if not sender:
                raise Exception(
                    "Sender account not found"
                )


            if not receiver:
                raise Exception(
                    "Receiver account not found"
                )


            if sender.id == receiver.id:
                raise Exception(
                    "Cannot transfer to same account"
                )


            # ===============================
            # VALIDATE AMOUNT
            # ===============================

            try:

                amount = Decimal(
                    str(amount)
                )

            except InvalidOperation:

                raise Exception(
                    "Invalid amount format"
                )


            if amount <= 0:

                raise Exception(
                    "Invalid amount"
                )


            if sender.balance < amount:

                raise Exception(
                    "Insufficient balance"
                )


            # ===============================
            # BALANCE UPDATE
            # ===============================

            sender.balance -= amount

            receiver.balance += amount


            # ===============================
            # TRANSACTION RECORD
            # ===============================

            transaction = Transaction(

                sender_account=sender.id,

                receiver_account=receiver.id,

                transaction_type="TRANSFER",

                amount=amount,

                currency=currency,

                status="SUCCESS"

            )


            db.session.add(transaction)

            db.session.flush()


            # ===============================
            # IDEMPOTENCY RECORD
            # ===============================

            if request_id:

                transaction_request = TransactionRequest(

                    request_id=request_id,

                    transaction_id=transaction.id,

                    status="COMPLETED"

                )

                db.session.add(
                    transaction_request
                )


            # ===============================
            # LEDGER ENTRIES
            # ===============================

            debit = LedgerEntry(

                transaction_id=transaction.id,

                account_id=sender.id,

                entry_type="DEBIT",

                amount=amount,

                balance_after=sender.balance

            )


            credit = LedgerEntry(

                transaction_id=transaction.id,

                account_id=receiver.id,

                entry_type="CREDIT",

                amount=amount,

                balance_after=receiver.balance

            )


            db.session.add(debit)

            db.session.add(credit)



            # ===============================
            # JOURNAL
            # ===============================

            journal = Journal(

                reference=f"TX-{transaction.id}",

                transaction_type="TRANSFER",

                amount=amount,

                currency=currency,

                status="POSTED"

            )


            db.session.add(journal)



            # ===============================
            # AUDIT
            # ===============================

            AuditTrail.log(

                action="TRANSFER_COMPLETED",

                username=username,

                metadata={

                    "transaction_id":
                        transaction.id,

                    "sender":
                        sender.id,

                    "receiver":
                        receiver.id,

                    "amount":
                        str(amount),

                    "currency":
                        currency

                }

            )


            db.session.commit()


            return transaction



        except Exception:

            db.session.rollback()

            raise
