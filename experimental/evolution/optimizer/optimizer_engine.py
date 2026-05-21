class OptimizerEngine:

    def optimize(

        self,

        knowledge
    ):

        actions = []

        if knowledge.get(
            "optimization"
        ):

            actions.append(
                "BOOST_WORKERS"
            )

        if knowledge.get(
            "security"
        ):

            actions.append(
                "ENABLE_LOCKDOWN"
            )

        return actions
