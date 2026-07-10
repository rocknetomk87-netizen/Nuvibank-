from flask import Flask

from core_bank.extensions import db, migrate
from core_bank.config import (
    SECRET_KEY,
    DATABASE_URL
)

from core_bank.models import User, Account, Transaction

from core_bank.routes.auth import auth_bp
from core_bank.routes.transactions import transactions_bp


def create_app():
    app = Flask(__name__)

    # CONFIGURAÇÕES
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # EXTENSÕES
    db.init_app(app)
    migrate.init_app(app, db)

    # BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)

    # HEALTH CHECK
    @app.route("/")
    def home():
        return {
            "status": "online",
            "system": "NUVIBANK CORE",
            "version": "1.0"
        }

    return app


app = create_app()
