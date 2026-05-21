from datetime import datetime

class AuditTrail:

    logs = []

    @classmethod
    def log(
        cls,
        action,
        username
    ):

        event = {

            "action":
                action,

            "username":
                username,

            "timestamp":
                str(datetime.utcnow())
        }

        cls.logs.append(event)

    @classmethod
    def get_logs(cls):

        return cls.logs
