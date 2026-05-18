class CNSDecisionEngine:

    @staticmethod
    def analyze(state):

        decisions = []

        if state["cpu"] > 80:

            decisions.append(
                "SCALE_WORKERS"
            )

        if state["memory"] > 85:

            decisions.append(
                "REDUCE_CACHE"
            )

        if state["fraud_alerts"] > 5:

            decisions.append(
                "ENABLE_MAX_SECURITY"
            )

        if state["requests"] > 1000:

            decisions.append(
                "ENABLE_LOAD_BALANCING"
            )

        return decisions
