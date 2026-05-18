from core.models import Wallet
from core.db import db


def get_wallet(user_id):

    return Wallet.query.filter_by(
        user_id=user_id
    ).first()


def create_wallet(user_id):

    wallet = Wallet(
        user_id=user_id
    )

    db.session.add(wallet)
    db.session.commit()

    return wallet
