class DetectionEngine:

    def detect(self, event):

        risk = event.get("risk")

        if risk == "HIGH":
            detected = True
        else:
            detected = False

        return {
            "event": event,
            "threat_detected": detected
        }
