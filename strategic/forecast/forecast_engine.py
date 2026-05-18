class ForecastEngine:

    def forecast_growth(

        self,

        users
    ):

        projected = (
            users * 1.35
        )

        return {

            "future_users":
            int(projected)
        }
