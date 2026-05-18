from core.db import get_db_connection


def transfer_money(sender, receiver, amount):

    conn = get_db_connection()

    cursor = conn.cursor()

    try:

        amount = float(amount)

        cursor.execute("""
        SELECT balance FROM users
        WHERE username = ?
        """, (sender,))

        sender_data = cursor.fetchone()

        if not sender_data:
            return {
                "success": False,
                "error": "Sender not found"
            }

        sender_balance = sender_data["balance"]

        if sender_balance < amount:
            return {
                "success": False,
                "error": "Insufficient funds"
            }

        cursor.execute("""
        SELECT * FROM users
        WHERE username = ?
        """, (receiver,))

        receiver_data = cursor.fetchone()

        if not receiver_data:
            return {
                "success": False,
                "error": "Receiver not found"
            }

        cursor.execute("""
        UPDATE users
        SET balance = balance - ?
        WHERE username = ?
        """, (
            amount,
            sender
        ))

        cursor.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE username = ?
        """, (
            amount,
            receiver
        ))

        cursor.execute("""
        INSERT INTO transactions (
            sender,
            receiver,
            amount
        )
        VALUES (?, ?, ?)
        """, (
            sender,
            receiver,
            amount
        ))

        conn.commit()

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        conn.close()


def get_transactions(username):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM transactions
    WHERE sender = ?
    OR receiver = ?
    ORDER BY created_at DESC
    """, (
        username,
        username
    ))

    data = cursor.fetchall()

    conn.close()

    return data
