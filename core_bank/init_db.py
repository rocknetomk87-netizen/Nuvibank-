from core_bank.core_app import create_app
from core_bank.core_app import db

app = create_app()

with app.app_context():

    db.create_all()

    print("NUVIBANK DATABASE INITIALIZED")
