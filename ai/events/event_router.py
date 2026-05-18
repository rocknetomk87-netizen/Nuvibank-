class EventRouter:

    @staticmethod
    def route(event_type):

        routes = {

            "LOGIN":
                "security",

            "TRANSFER":
                "risk_engine",

            "WITHDRAW":
                "fraud_engine",

            "PAYMENT":
                "payment_engine"
        }

        return routes.get(
            event_type,
            "unknown"
        )
