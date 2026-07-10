from datetime import datetime, timezone
from core_bank.extensions import db


class Journal(db.Model):

    __tablename__ = "journals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reference = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    transaction_type = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(18, 2),
        nullable=False
    )

    currency = db.Column(
        db.String(10),
        default="AOA"
    )

    status = db.Column(
        db.String(20),
        default="POSTED"
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
