class PredictEngine:

    def predict_risk(

        self,

        failed_logins
    ):

        if failed_logins > 5:

            return "HIGH_RISK"

        return "NORMAL"
