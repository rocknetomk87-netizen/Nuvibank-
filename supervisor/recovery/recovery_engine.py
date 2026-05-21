class RecoveryEngine:

    def recover(self, report):

        recoveries = []

        for item in report:

            if item["health"] == "FAILED":

                recoveries.append({

                    "system": item["system"],

                    "recovery": "RESTART_TRIGGERED"
                })

        return recoveries
