from datetime import datetime


class PoolRuntime:

    def status(self):

        return {
            "runtime": "WORKER_POOL_ACTIVE",
            "timestamp": str(datetime.utcnow()),
            "status": "RUNNING"
        }
