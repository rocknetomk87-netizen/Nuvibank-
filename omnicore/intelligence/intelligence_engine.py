class IntelligenceEngine:

    def analyze(self, event):

        risk = event.get("risk")

        if risk == "HIGH":
            decision = "LOCKDOWN"

        elif risk == "MEDIUM":
            decision = "MONITOR"

        else:
            decision = "ALLOW"

        return {
            "event": event,
            "decision": decision,
            "intelligence": "ACTIVE"
        }
