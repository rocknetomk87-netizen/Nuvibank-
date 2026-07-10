from core_bank.core_app import create_app, db
from core_bank.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    # =========================
    # ROCK USER
    # =========================

    rock_exists = User.query.filter_by(
        email="rock@nuvibank.com"
    ).first()

    if not rock_exists:

        rock = User(
            username="rock",
            email="rock@nuvibank.com",
            password=generate_password_hash("123456"),
            balance=1000.0
        )

        db.session.add(rock)

    # =========================
    # ALICE USER
    # =========================

    alice_exists = User.query.filter_by(
        email="alice@nuvibank.com"
    ).first()

    if not alice_exists:

        alice = User(
            username="alice",
            email="alice@nuvibank.com",
            password=generate_password_hash("123456"),
            balance=500.0
        )

        db.session.add(alice)

    db.session.commit()

    print("✅ DATABASE CRIADA COM SUCESSO")
