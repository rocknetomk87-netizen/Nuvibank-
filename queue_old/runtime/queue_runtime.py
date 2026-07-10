from datetime import datetime


class QueueRuntime:

    def status(self):

        return {
            "runtime": "QUEUE_SYSTEM_ACTIVE",
            "timestamp": str(datetime.utcnow()),
            "status": "RUNNING"
        }
