from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from core_bank.config import Config

db = SQLAlchemy()

jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    jwt.init_app(app)

    from core_bank.api.v1.server import register_routes

    register_routes(app)

    return app
