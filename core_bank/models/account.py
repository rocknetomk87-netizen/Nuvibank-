from core_bank.extensions import db
import uuid


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    account_type = db.Column(
        db.String(50),
        default="savings"
    )

    balance = db.Column(
        db.Numeric(18, 2),
        default=0
    )

    currency = db.Column(
        db.String(10),
        default="AOA"
    )

    status = db.Column(
        db.String(20),
        default="active"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
