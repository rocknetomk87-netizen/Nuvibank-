class AnalysisEngine:

    def analyze(self, event):

        if event["risk"] == "HIGH":

            return {
                "threat": True,
                "action": "LOCKDOWN"
            }

        return {
            "threat": False,
            "action": "MONITOR"
        }
