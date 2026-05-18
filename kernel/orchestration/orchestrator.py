class Orchestrator:

    def route(

        self,

        event
    ):

        routes = {

            "FRAUD":
            "IMMUNE_SYSTEM",

            "TRANSFER":
            "FINANCE_CORE",

            "AI_ANALYSIS":
            "NEURAL_ENGINE",

            "SCALING":
            "SCALING_ENGINE"
        }

        return routes.get(
            event,
            "DEFAULT_CORE"
        )
