import uuid
from datetime import datetime

class LedgerEngine:

    ledger = []

    @classmethod
    def record(
        cls,
        sender,
        receiver,
        amount
    ):

        transaction = {

            "tx_id":
                str(uuid.uuid4()),

            "sender":
                sender,

            "receiver":
                receiver,

            "amount":
                amount,

            "timestamp":
                str(datetime.utcnow())
        }

        cls.ledger.append(
            transaction
        )

        return transaction

    @classmethod
    def get_ledger(cls):

        return cls.ledger
