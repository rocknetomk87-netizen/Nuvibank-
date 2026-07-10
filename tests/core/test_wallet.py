from wallet.validator import validate_balance


class MockWallet:
    available_balance = 500


wallet = MockWallet()

print(
    validate_balance(wallet, 100)
)

print(
    validate_balance(wallet, 1000)
)
