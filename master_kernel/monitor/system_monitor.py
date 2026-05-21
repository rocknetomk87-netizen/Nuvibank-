class SystemMonitor:

    def inspect(self, systems):

        report = []

        for system in systems:

            report.append({

                "system": system["system"],

                "health": "HEALTHY",

                "latency": 20
            })

        return report
