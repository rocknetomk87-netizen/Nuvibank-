import jwt
import datetime
import os

from dotenv import load_dotenv

load_dotenv()

def generate_token(username, role):

    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    secret = os.getenv("JWT_SECRET")

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256"
    )

    return token


def verify_token(token):

    try:

        secret = os.getenv("JWT_SECRET")

        data = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )

        return data

    except:
        return None
