from datetime import datetime
from core_bank.database.db_engine import db


class JournalEntry(db.Model):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.Integer, nullable=False)

    account_type = db.Column(db.String(50), nullable=False)

    account_id = db.Column(db.Integer, nullable=False)

    entry_type = db.Column(db.String(10), nullable=False)
    # debit or credit

    amount = db.Column(db.Float, nullable=False)

    currency = db.Column(db.String(10), default="USD")

    description = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "account_type": self.account_type,
            "account_id": self.account_id,
            "entry_type": self.entry_type,
            "amount": self.amount,
            "currency": self.currency,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
