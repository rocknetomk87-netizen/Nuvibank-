from core_bank.core_app import db
from datetime import datetime


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(
        db.Integer,
        nullable=True
    )

    receiver_id = db.Column(
        db.Integer,
        nullable=True
    )

    transaction_type = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "created_at": str(self.created_at)
        }
