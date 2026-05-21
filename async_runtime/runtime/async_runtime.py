from datetime import datetime


class AsyncRuntime:

    def status(self):

        return {
            "runtime": "ASYNC_RUNTIME_ACTIVE",
            "timestamp": str(datetime.utcnow()),
            "status": "RUNNING"
        }
