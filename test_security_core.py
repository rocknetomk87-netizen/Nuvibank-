from core_bank.security.passwords import hash_password, verify_password
from core_bank.security.jwt import generate_token
from core_bank.models.user import User


def test_password_hashing():
    password = "SenhaForte123@"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("senha_errada", hashed) is False

    print("PASSWORD SECURITY: OK")


def test_jwt_generation():
    user = User(
        id=1,
        username="admin",
        email="admin@nuvibank.com",
        password="hashed"
    )

    token = generate_token(user)

    assert token is not None
    assert isinstance(token, str)
    assert len(token.split(".")) == 3

    print("JWT SECURITY: OK")


if __name__ == "__main__":
    test_password_hashing()
    test_jwt_generation()
    print("NUVIBANK SECURITY CORE: PASSED")
