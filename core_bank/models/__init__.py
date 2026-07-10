"""
NUVIBANK CORE
Model Registry

Responsável por centralizar todos os modelos SQLAlchemy.
"""

# User & Identity
from core_bank.models.user import User

# Banking Core
from core_bank.models.account import Account

# Transactions
from core_bank.models.transaction import Transaction

# Idempotency / Request Protection
from core_bank.models.transaction_request import TransactionRequest


__all__ = [
    "User",
    "Account",
    "Transaction",
    "TransactionRequest",
]
