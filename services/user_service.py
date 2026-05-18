from core.db import get_db_connection

import bcrypt


# =========================================================
# CREATE USER
# =========================================================

def create_user(username, password):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = ?
    """, (username,))

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return {
            "success": False,
            "error": "User already exists"
        }

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""
    INSERT INTO users (
        username,
        password,
        balance,
        role
    )
    VALUES (?, ?, ?, ?)
    """, (
        username,
        hashed_password,
        1000,
        "user"
    ))

    conn.commit()

    conn.close()

    return {
        "success": True,
        "message": "Account created"
    }


# =========================================================
# GET USER
# =========================================================

def get_user_by_username(username):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# LOGIN
# =========================================================

def authenticate_user(username, password):

    user = get_user_by_username(username)

    if not user:

        return {
            "success": False,
            "error": "User not found"
        }

    valid_password = bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    )

    if not valid_password:

        return {
            "success": False,
            "error": "Invalid password"
        }

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "username": user["username"],
            "balance": user["balance"],
            "role": user["role"]
        }
    }
