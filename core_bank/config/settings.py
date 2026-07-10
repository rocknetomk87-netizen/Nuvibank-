import os


class Config:

    # APP
    APP_NAME = "NUVIBANK CORE"

    DEBUG = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "NUVIBANK_ULTRA_SECRET"
    )

    # JWT
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "ULTRA_NUVIBANK_SECRET"
    )

    JWT_ACCESS_TOKEN_EXPIRES = 86400

    # DATABASE
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///nuvibank.db"
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # REDIS
    REDIS_HOST = "127.0.0.1"

    REDIS_PORT = 6379

    REDIS_URL = "redis://127.0.0.1:6379"

    # RATE LIMIT
    RATELIMIT_STORAGE_URI = "redis://127.0.0.1:6379"

    # SECURITY
    BCRYPT_LOG_ROUNDS = 12

    # LOGGING
    LOG_LEVEL = "INFO"

    LOG_FILE = "logs/runtime.log"
