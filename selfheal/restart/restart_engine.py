class RestartEngine:

    def restart(self, failures):

        restarted = []

        for system in failures:

            restarted.append({

                "system": system,

                "restart": "RESTART_TRIGGERED",

                "status": "ACTIVE"
            })

        return restarted
