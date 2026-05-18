from finance.ledger.ledger_engine import LedgerEngine

from finance.audit.audit_trail import AuditTrail

from finance.core.transaction_validator import TransactionValidator


valid = TransactionValidator.validate(
    sender_balance=10000,
    amount=5000
)

print(valid)

if valid:

    tx = LedgerEngine.record(
        sender="rock",
        receiver="alex",
        amount=5000
    )

    AuditTrail.log(
        action="TRANSFER",
        username="rock"
    )

    print(tx)

    print(
        LedgerEngine.get_ledger()
    )

    print(
        AuditTrail.get_logs()
    )
