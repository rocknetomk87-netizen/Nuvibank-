from datetime import datetime, timezone
import uuid

from core_bank.extensions import db


class LedgerEntry(db.Model):

    """
    Lançamento contábil do NUVIBANK Core.

    Cada movimento financeiro gera uma entrada:
    DEBIT ou CREDIT.
    """

    __tablename__ = "ledger_entries"


    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    transaction_id = db.Column(
        db.Integer,
        nullable=False
    )


    account_id = db.Column(
        db.String(36),
        nullable=False
    )


    entry_type = db.Column(
        db.String(20),
        nullable=False
    )


    amount = db.Column(
        db.Numeric(18, 2),
        nullable=False
    )


    balance_after = db.Column(
        db.Numeric(18, 2),
        nullable=False
    )


    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    def to_dict(self):

        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "entry_type": self.entry_type,
            "amount": str(self.amount),
            "balance_after": str(self.balance_after),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


    def __repr__(self):

        return (
            f"<LedgerEntry "
            f"{self.entry_type} "
            f"{self.amount}>"
        )
