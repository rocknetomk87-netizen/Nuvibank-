from datetime import datetime

class SystemLogger:

    def log(self, level, message):

        return {
            "timestamp": str(datetime.utcnow()),
            "layer": "SYSTEM",
            "level": level,
            "message": message
        }
