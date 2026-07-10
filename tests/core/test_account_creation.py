import pytest

from core_bank.app_factory import create_app
from core_bank.extensions import db
from core_bank.models import User, Account


@pytest.fixture
def app():

    app = create_app()

    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


def test_create_user_with_account(app):

    with app.app_context():

        user = User(
            username="test_user",
            email="test@nuvibank.com",
            password="hashed_password"
        )

        db.session.add(user)
        db.session.commit()


        account = Account(
            user_id=user.id,
            account_type="savings",
            balance=1000,
            currency="AOA"
        )

        db.session.add(account)
        db.session.commit()


        saved_user = User.query.filter_by(
            username="test_user"
        ).first()


        assert saved_user is not None

        assert len(saved_user.accounts) == 1

        assert saved_user.accounts[0].balance == 1000
