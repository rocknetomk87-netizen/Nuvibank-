class LearningEngine:

    def learn(

        self,

        metrics
    ):

        knowledge = {}

        if metrics["cpu"] > 80:

            knowledge["optimization"] = (
                "CPU_HIGH"
            )

        if metrics["fraud_alerts"] > 5:

            knowledge["security"] = (
                "INCREASE_SECURITY"
            )

        return knowledge
