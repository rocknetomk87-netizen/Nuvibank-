import jwt

from datetime import datetime, timezone, timedelta

from core_bank.config import (
    SECRET_KEY,
    JWT_EXPIRE_HOURS
)


def generate_token(user):

    payload = {

        "user_id": user.id,

        "email": user.email,

        "iat": datetime.now(timezone.utc),

        "exp": datetime.now(timezone.utc) + timedelta(
            hours=JWT_EXPIRE_HOURS
        )
    }


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )
