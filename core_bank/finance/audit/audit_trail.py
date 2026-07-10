from datetime import datetime, timezone
import uuid


class AuditTrail:
    """
    Sistema de auditoria do NUVIBANK.

    Regista eventos internos:
    - ação executada
    - utilizador responsável
    - momento UTC
    - identificador único do evento
    """

    logs = []


    @classmethod
    def log(
        cls,
        action,
        username,
        metadata=None
    ):

        event = {

            "event_id": str(uuid.uuid4()),

            "action": action,

            "username": username,

            "metadata": metadata or {},

            "timestamp": datetime.now(timezone.utc).isoformat()
        }


        cls.logs.append(event)


        return event


    @classmethod
    def get_logs(cls):

        return cls.logs
