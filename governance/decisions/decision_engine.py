class DecisionEngine:

    def decide(

        self,

        risk,
        load
    ):

        actions = []

        if risk >= 8:

            actions.append(
                "LOCKDOWN"
            )

            actions.append(
                "ENABLE_MFA"
            )

        if load >= 8:

            actions.append(
                "SCALE_UP"
            )

        return actions
