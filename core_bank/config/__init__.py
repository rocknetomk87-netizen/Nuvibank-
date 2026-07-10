import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "NUVIBANK_CORE_SECURITY_KEY_2026_PRODUCTION_CHANGE_ME_64_CHARACTERS_MINIMUM"
)


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    SECRET_KEY
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///nuvibank.db"
)


JWT_EXPIRE_HOURS = int(
    os.getenv(
        "JWT_EXPIRE_HOURS",
        "24"
    )
)


FLASK_ENV = os.getenv(
    "FLASK_ENV",
    "development"
)
