from datetime import datetime, timezone
from core_bank.extensions import db


class TransactionLimit(db.Model):

    __tablename__ = "transaction_limits"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    daily_limit = db.Column(
        db.Numeric(18, 2),
        default=1000000
    )

    single_transaction_limit = db.Column(
        db.Numeric(18, 2),
        default=500000
    )

    daily_used = db.Column(
        db.Numeric(18, 2),
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda:
        datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda:
        datetime.now(timezone.utc),
        onupdate=lambda:
        datetime.now(timezone.utc)
    )


    def can_transfer(self, amount):

        if amount > self.single_transaction_limit:
            return False

        if (
            self.daily_used + amount
            > self.daily_limit
        ):
            return False

        return True


    def consume(self, amount):

        self.daily_used += amount
