class DecisionEngine:

    def decide(

        self,

        awareness
    ):

        decisions = []

        if "SECURITY_CRITICAL" in awareness:

            decisions.append(
                "ENABLE_LOCKDOWN"
            )

        if "FRAUD_ACTIVITY" in awareness:

            decisions.append(
                "ENABLE_MAX_MONITORING"
            )

        return decisions
