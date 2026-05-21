class TransactionValidator:

    @staticmethod
    def validate(
        sender_balance,
        amount
    ):

        if amount <= 0:

            return False

        if sender_balance < amount:

            return False

        return True
