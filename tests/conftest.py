import pytest

from core_bank.app_factory import create_app
from core_bank.extensions import db


@pytest.fixture
def app():

    app = create_app()

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()
