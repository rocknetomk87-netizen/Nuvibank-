from datetime import datetime


class EventRuntime:

    def runtime_status(self):

        return {
            "runtime": "EVENT_BUS_ACTIVE",
            "timestamp": str(datetime.utcnow()),
            "status": "RUNNING"
        }
