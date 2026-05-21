class RepairEngine:

    def repair(self, failures):

        repaired = []

        for system in failures:

            repaired.append({

                "system": system,

                "repair": "AUTO_REPAIR",

                "status": "COMPLETED"
            })

        return repaired
