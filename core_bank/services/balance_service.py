from decimal import Decimal

from core_bank.extensions import db
from core_bank.models.account import Account
from core_bank.ledger.models.ledger_entry import LedgerEntry


class BalanceService:


    @staticmethod
    def deposit(account_id, amount):

        account = Account.query.get(account_id)

        if not account:
            raise Exception("Account not found")


        amount = Decimal(amount)


        account.balance += amount


        entry = LedgerEntry(
            transaction_id=None,
            account_id=account.id,
            entry_type="CREDIT",
            amount=amount,
            balance_after=account.balance
        )


        db.session.add(entry)
        db.session.commit()


        return account.balance



    @staticmethod
    def withdraw(account_id, amount):

        account = Account.query.get(account_id)

        if not account:
            raise Exception("Account not found")


        amount = Decimal(amount)


        if account.balance < amount:
            raise Exception("Insufficient balance")


        account.balance -= amount


        entry = LedgerEntry(
            transaction_id=None,
            account_id=account.id,
            entry_type="DEBIT",
            amount=amount,
            balance_after=account.balance
        )


        db.session.add(entry)
        db.session.commit()


        return account.balance
