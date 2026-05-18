cursor.execute("""
CREATE TABLE IF NOT EXISTS ledger_entries (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_id TEXT UNIQUE,

    user_id INTEGER,

    entry_type TEXT,

    amount REAL,

    balance_before REAL,

    balance_after REAL,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    available_balance = db.Column(
        db.Float,
        default=0.0
    )

    pending_balance = db.Column(
        db.Float,
        default=0.0
    )

    locked_balance = db.Column(
        db.Float,
        default=0.0
    )

    currency = db.Column(
        db.String(10),
        default="USD"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
