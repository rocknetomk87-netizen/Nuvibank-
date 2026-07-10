from core_bank.app_factory import create_app


def test_app_creation():

    app = create_app()

    assert app is not None
