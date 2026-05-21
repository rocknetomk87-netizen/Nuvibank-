class AwarenessEngine:

    def analyze(

        self,

        state
    ):

        awareness = []

        if state["security"] == "HIGH":

            awareness.append(
                "SECURITY_CRITICAL"
            )

        if state["fraud_alerts"] >= 2:

            awareness.append(
                "FRAUD_ACTIVITY"
            )

        return awareness
