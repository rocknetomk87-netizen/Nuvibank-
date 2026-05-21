from core_bank.database.db_engine import db


class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    balance = db.Column(db.Float, default=0.0)

    currency = db.Column(db.String(10), default="USD")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Wallet {self.id}>"
