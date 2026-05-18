class DecisionEngine:

    @staticmethod
    def decide(risk_level,
               trust_score):

        if risk_level == "HIGH":

            return {
                "action": "BLOCK",
                "message": "High risk detected"
            }

        if trust_score < 40:

            return {
                "action": "VERIFY",
                "message": "Extra verification required"
            }

        return {
            "action": "ALLOW",
            "message": "Operation approved"
        }
