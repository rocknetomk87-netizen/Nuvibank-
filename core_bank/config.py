import os

class Config:

    SECRET_KEY = "NUVIBANK_SECRET_CORE"

    JWT_SECRET_KEY = "NUVIBANK_JWT_SUPER_SECRET"

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://localhost/nuvibank"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
