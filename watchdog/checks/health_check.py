class HealthCheck:

    def inspect(self, systems):

        health_report = []

        for system in systems:

            latency = system.get(
                "latency",
                0
            )

            if latency > 100:

                status = "DEGRADED"

            else:

                status = "HEALTHY"

            health_report.append({

                "system": system["name"],

                "latency": latency,

                "health": status
            })

        return health_report
