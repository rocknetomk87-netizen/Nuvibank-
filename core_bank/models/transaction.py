from datetime import datetime, timezone

from core_bank.extensions import db


class Transaction(db.Model):
    """
    Modelo principal de transações financeiras do NUVIBANK Core.

    Responsável pelo armazenamento persistente
    dos movimentos financeiros entre contas.
    """

    __tablename__ = "transactions"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    sender_account = db.Column(
        db.String(36),
        nullable=False
    )


    receiver_account = db.Column(
        db.String(36),
        nullable=False
    )


    transaction_type = db.Column(
        db.String(50),
        nullable=False,
        default="TRANSFER"
    )


    amount = db.Column(
        db.Numeric(18, 2),
        nullable=False
    )


    currency = db.Column(
        db.String(10),
        nullable=False,
        default="AOA"
    )


    status = db.Column(
        db.String(20),
        nullable=False,
        default="SUCCESS"
    )


    description = db.Column(
        db.String(255),
        nullable=True
    )


    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    def to_dict(self):

        return {
            "id": self.id,
            "sender_account": self.sender_account,
            "receiver_account": self.receiver_account,
            "transaction_type": self.transaction_type,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status,
            "description": self.description,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            )
        }


    def __repr__(self):

        return (
            f"<Transaction {self.id} "
            f"{self.transaction_type} "
            f"{self.amount}>"
        )
