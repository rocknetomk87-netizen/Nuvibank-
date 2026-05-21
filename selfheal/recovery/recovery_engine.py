class RecoveryEngine:

    def recover(self, failures):

        recovered = []

        for system in failures:

            recovered.append({

                "system": system,

                "recovery": "RECOVERED",

                "status": "SUCCESS"
            })

        return recovered
