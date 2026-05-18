def validate_balance(wallet, amount):

    if wallet.available_balance < amount:
        return False

    return True
