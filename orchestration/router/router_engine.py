class RouterEngine:

    def route(self, event):

        routes = {

            "FRAUD":
            "IMMUNE_SYSTEM",

            "TRANSFER":
            "CONSENSUS_CORE",

            "FAILED_LOGIN":
            "SENTINEL_CORE"
        }

        return routes.get(
            event,
            "DEFAULT_CORE"
        )
