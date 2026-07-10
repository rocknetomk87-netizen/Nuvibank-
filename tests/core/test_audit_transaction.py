from core_bank.finance.audit.audit_trail import AuditTrail
from core_bank.finance.core.transaction_service import TransactionService
from core_bank.models.account import Account
from core_bank.extensions import db


def test_audit_created_after_transfer(app):

    with app.app_context():

        sender = Account(
            user_id=1,
            balance=1000
        )

        receiver = Account(
            user_id=2,
            balance=100
        )


        db.session.add(sender)
        db.session.add(receiver)

        db.session.commit()


        TransactionService.transfer(
            sender.id,
            receiver.id,
            250
        )


        logs = AuditTrail.get_logs()


        assert len(logs) > 0


        last_event = logs[-1]


        assert last_event["action"] == "TRANSFER_COMPLETED"

        assert "transaction_id" in last_event["metadata"]

        assert last_event["metadata"]["amount"] == "250"
