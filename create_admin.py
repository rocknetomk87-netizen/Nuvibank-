from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    user = User.query.filter_by(username="admin").first()

    if user:
        db.session.delete(user)
        db.session.commit()

    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        balance=100000
    )

    db.session.add(admin)
    db.session.commit()

    print("ADMIN NOVO CRIADO")
