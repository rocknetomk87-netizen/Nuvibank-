from datetime import datetime
from core_bank.database.db_engine import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    sender_wallet_id = db.Column(
        db.Integer,
        nullable=False
    )

    receiver_wallet_id = db.Column(
        db.Integer,
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    transaction_type = db.Column(
        db.String(50),
        default="transfer"
    )

    status = db.Column(
        db.String(20),
        default="success"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "sender_wallet_id": self.sender_wallet_id,
            "receiver_wallet_id": self.receiver_wallet_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "status": self.status,
            "created_at": str(self.created_at)
        }
