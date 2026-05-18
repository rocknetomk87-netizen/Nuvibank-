from datetime import datetime

class SecurityLogger:

    def alert(self, threat, risk):

        return {
            "timestamp": str(datetime.utcnow()),
            "layer": "SECURITY",
            "threat": threat,
            "risk": risk,
            "status": "ALERT_TRIGGERED"
        }
