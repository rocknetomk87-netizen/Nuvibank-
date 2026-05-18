class PredictEngine:

    def predict_next_actions(

        self,

        user_profile
    ):

        predictions = []

        if user_profile.get(
            "avg_transfer"
        ):

            predictions.append(
                "TRANSFER"
            )

        if user_profile.get(
            "daily_login"
        ):

            predictions.append(
                "BALANCE_CHECK"
            )

        return predictions
