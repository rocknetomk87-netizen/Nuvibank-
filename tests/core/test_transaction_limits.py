from decimal import Decimal

from core_bank.models.transaction_limit import TransactionLimit


def test_transaction_limit_validation():

    limit = TransactionLimit(
        user_id=1,
        daily_limit=Decimal("1000"),
        single_transaction_limit=Decimal("500"),
        daily_used=Decimal("0")
    )


    assert limit.can_transfer(
        Decimal("100")
    )


    assert not limit.can_transfer(
        Decimal("600")
    )


    limit.consume(
        Decimal("300")
    )


    assert limit.daily_used == Decimal("300")
