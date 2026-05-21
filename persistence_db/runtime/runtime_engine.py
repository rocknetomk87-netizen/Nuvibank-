from datetime import datetime


class RuntimeEngine:

    def status(self):

        return {

            "runtime": "PERSISTENCE_DB_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
