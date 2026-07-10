import uuid
from datetime import datetime, timezone


class LedgerEngine:
    """
    Ledger Engine experimental do NUVIBANK.

    Regista eventos financeiros básicos.
    O ledger principal de dupla entrada permanece
    no módulo core_bank.ledger.
    """

    ledger = []


    @classmethod
    def record(
        cls,
        sender,
        receiver,
        amount
    ):

        transaction = {

            "tx_id": str(uuid.uuid4()),

            "sender": sender,

            "receiver": receiver,

            "amount": str(amount),

            "timestamp": datetime.now(timezone.utc).isoformat()
        }


        cls.ledger.append(
            transaction
        )


        return transaction


    @classmethod
    def get_ledger(cls):

        return cls.ledger
