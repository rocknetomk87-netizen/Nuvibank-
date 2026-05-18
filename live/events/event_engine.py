class EventEngine:

    def next_event(self):

        return {
            "type": "FRAUD_ALERT",
            "risk": "HIGH",
            "user": "rock"
        }
