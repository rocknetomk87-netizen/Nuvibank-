from audit.core.audit_core import (
    AuditCore
)

core = AuditCore()

core.log_event(
    "USER_LOGIN"
)

core.log_event(
    "TRANSFER_5000"
)

core.log_event(
    "FRAUD_ALERT"
)

print(
    core.logs()
)
