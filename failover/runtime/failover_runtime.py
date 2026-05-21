from datetime import datetime


class FailoverRuntime:

    def status(self):

        return {

            "runtime": "FAILOVER_CLUSTER_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
