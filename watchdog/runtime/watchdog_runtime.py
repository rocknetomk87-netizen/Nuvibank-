from datetime import datetime


class WatchdogRuntime:

    def status(self):

        return {

            "runtime": "WATCHDOG_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
