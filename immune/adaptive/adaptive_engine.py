class AdaptiveEngine:

    def adapt(self, quarantine):

        if quarantine.get("isolated"):
            return {
                "adaptive_mode": "DEFENSE",
                "learning": "ACTIVE",
                "response": "AUTONOMOUS_LOCKDOWN"
            }

        return {
            "adaptive_mode": "NORMAL",
            "learning": "PASSIVE",
            "response": "MONITORING"
        }
