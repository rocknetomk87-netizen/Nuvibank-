from datetime import datetime


class SupervisorRuntime:

    def status(self):

        return {

            "runtime": "SUPERVISOR_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
