from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    user_exists = User.query.filter_by(username="user1").first()

    if not user_exists:

        user = User(
            username="user1",
            password=generate_password_hash("123456"),
            balance=5000
        )

        db.session.add(user)
        db.session.commit()

        print("✅ USER1 CRIADO")

    else:
        print("⚠️ USER1 JÁ EXISTE")
