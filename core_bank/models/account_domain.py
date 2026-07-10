from datetime import datetime
from decimal import Decimal
import uuid


class AccountStatus:
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"


class AccountType:
    SAVINGS = "savings"
    CHECKING = "checking"
    BUSINESS = "business"


class Account:
    """
    Núcleo de conta bancária do sistema NUVIBANK Core.
    Responsável por saldo, estado e operações financeiras base.
    """

    def __init__(
        self,
        user_id: str,
        account_type: str = AccountType.SAVINGS,
        initial_balance: Decimal = Decimal("0.00"),
        currency: str = "AOA",
    ):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.account_type = account_type
        self.balance = Decimal(initial_balance)
        self.currency = currency

        self.status = AccountStatus.ACTIVE

        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        self.transaction_count = 0
        self.last_transaction_at = None

    # =========================
    # CORE OPERATIONS
    # =========================

    def deposit(self, amount: Decimal):
        self._validate_active()

        amount = self._validate_amount(amount)

        self.balance += amount
        self._touch()

        return self._log("deposit", amount)

    def withdraw(self, amount: Decimal):
        self._validate_active()

        amount = self._validate_amount(amount)

        if self.balance < amount:
            raise ValueError("Saldo insuficiente")

        self.balance -= amount
        self._touch()

        return self._log("withdraw", amount)

    def transfer_out(self, amount: Decimal):
        """
        Usado quando o dinheiro sai da conta (transferência externa).
        """
        return self.withdraw(amount)

    def transfer_in(self, amount: Decimal):
        """
        Usado quando o dinheiro entra por transferência.
        """
        return self.deposit(amount)

    # =========================
    # STATE CONTROL
    # =========================

    def freeze(self):
        self.status = AccountStatus.FROZEN
        self._touch()

    def activate(self):
        self.status = AccountStatus.ACTIVE
        self._touch()

    def close(self):
        if self.balance != 0:
            raise ValueError("Conta só pode ser fechada com saldo zero")
        self.status = AccountStatus.CLOSED
        self._touch()

    # =========================
    # INTERNAL LOGIC
    # =========================

    def _validate_active(self):
        if self.status != AccountStatus.ACTIVE:
            raise ValueError(f"Conta não está ativa: {self.status}")

    def _validate_amount(self, amount: Decimal) -> Decimal:
        amount = Decimal(amount)

        if amount <= 0:
            raise ValueError("Valor deve ser maior que zero")

        return amount

    def _log(self, operation: str, amount: Decimal):
        self.transaction_count += 1
        self.last_transaction_at = datetime.utcnow()

        return {
            "account_id": self.id,
            "operation": operation,
            "amount": str(amount),
            "balance_after": str(self.balance),
            "timestamp": self.last_transaction_at.isoformat(),
        }

    def _touch(self):
        self.updated_at = datetime.utcnow()

    # =========================
    # SERIALIZATION
    # =========================

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_type": self.account_type,
            "balance": str(self.balance),
            "currency": self.currency,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "transaction_count": self.transaction_count,
            "last_transaction_at": (
                self.last_transaction_at.isoformat()
                if self.last_transaction_at
                else None
            ),
        }

    @staticmethod
    def from_dict(data: dict):
        acc = Account(
            user_id=data["user_id"],
            account_type=data.get("account_type", AccountType.SAVINGS),
            initial_balance=Decimal(data.get("balance", "0")),
            currency=data.get("currency", "AOA"),
        )

        acc.id = data["id"]
        acc.status = data.get("status", AccountStatus.ACTIVE)
        acc.transaction_count = data.get("transaction_count", 0)

        return acc
