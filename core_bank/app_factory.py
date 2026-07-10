from flask import Flask

from core_bank.extensions import db, migrate


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///nuvibank.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    migrate.init_app(app, db)


    # Registrar modelos
    from core_bank.models import (
        User,
        Account,
        Transaction
    )


    # Registrar Ledger
    from core_bank.ledger.models import (
        Journal,
        LedgerEntry
    )


    with app.app_context():

        db.create_all()


    return app
