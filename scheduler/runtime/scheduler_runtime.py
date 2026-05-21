from datetime import datetime


class SchedulerRuntime:

    def status(self):

        return {
            "runtime": "SCHEDULER_ACTIVE",
            "timestamp": str(datetime.utcnow()),
            "status": "RUNNING"
        }
