from datetime import datetime


class ReplicationRuntime:

    def status(self):

        return {

            "runtime": "STATE_REPLICATION_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
