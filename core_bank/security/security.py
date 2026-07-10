from werkzeug.security import generate_password_hash


def secure_password(password):

    return generate_password_hash(
        password,
        method="pbkdf2:sha256",
        salt_length=16
    )
