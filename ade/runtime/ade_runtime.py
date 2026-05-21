from datetime import datetime


class ADERuntime:

    def status(self):

        return {

            "runtime": "ADE_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
