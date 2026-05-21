class PredictEngine:

    def predict(

        self,

        patterns
    ):

        if 22 in patterns["fraud_hours"]:

            return {

                "high_risk_hour": 22,

                "action": "ENABLE_MAX_SECURITY"
            }

        return {

            "status": "NORMAL"
        }
