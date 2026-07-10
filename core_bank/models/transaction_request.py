from datetime import datetime, timezone
from core_bank.extensions import db


class TransactionRequest(db.Model):

    __tablename__ = "transaction_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    idempotency_key = db.Column(
        db.String(128),
        unique=True,
        nullable=False,
        index=True
    )

    transaction_id = db.Column(
        db.Integer,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        default="PROCESSING"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


    def to_dict(self):

        return {
            "id": self.id,
            "idempotency_key": self.idempotency_key,
            "transaction_id": self.transaction_id,
            "status": self.status,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
