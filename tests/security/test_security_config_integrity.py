import os

from core_bank.config import (
    SECRET_KEY,
    JWT_SECRET_KEY
)


def test_secret_key_strength():

    assert SECRET_KEY is not None

    assert len(SECRET_KEY) >= 32



def test_jwt_secret_key_strength():

    assert JWT_SECRET_KEY is not None

    assert len(JWT_SECRET_KEY) >= 32



def test_no_hardcoded_route_secrets():

    routes_path = "core_bank/routes"

    forbidden = [
        'SECRET_KEY = "NUVIBANK_ULTRA_SECRET_2026"',
        "SECRET_KEY='NUVIBANK_ULTRA_SECRET_2026'"
    ]


    for root, _, files in os.walk(routes_path):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(
                    root,
                    file
                )

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()


                for secret in forbidden:

                    assert secret not in content, (
                        f"Hardcoded secret found in {path}"
                    )
