class SystemMonitor:

    def inspect(self, systems):

        report = []

        for system in systems:

            report.append({

                "system": system["name"],

                "status": system["status"],

                "health": (
                    "HEALTHY"
                    if system["status"] == "RUNNING"
                    else "FAILED"
                )
            })

        return report
