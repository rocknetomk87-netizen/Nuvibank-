from datetime import datetime

class RuntimeLogger:

    def runtime(self, cycle, status):

        return {
            "timestamp": str(datetime.utcnow()),
            "layer": "RUNTIME",
            "cycle": cycle,
            "status": status
        }
