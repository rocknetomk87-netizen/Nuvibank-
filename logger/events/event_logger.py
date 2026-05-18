from datetime import datetime

class EventLogger:

    def event(self, event):

        return {
            "timestamp": str(datetime.utcnow()),
            "layer": "EVENT",
            "event": event,
            "status": "RECORDED"
        }
