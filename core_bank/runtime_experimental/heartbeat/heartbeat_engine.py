from datetime import datetime


class HeartbeatEngine:
    def beat(self):
        return {
            "alive": True,
            "timestamp": str(datetime.utcnow()),
            "pulse": "STABLE"
        }
