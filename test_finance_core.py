from core_bank.finance.ledger.ledger_engine import LedgerEngine
from core_bank.finance.audit.audit_trail import AuditTrail
from core_bank.finance.core.transaction_validator import TransactionValidator

print("=== FINANCE CORE TEST ===")

valid = TransactionValidator.validate(
    sender_balance=10000,
    amount=5000
)

print("Validation:", valid)

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

    print("Transaction:")
    print(tx)

    print()

    print("Audit Logs:")
    print(AuditTrail.get_logs())

    print()

    print("Ledger:")
    print(LedgerEngine.get_ledger())

print("=== TEST COMPLETE ===")
