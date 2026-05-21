class AlertEngine:

    def process(self, report):

        alerts = []

        for item in report:

            if item["health"] != "HEALTHY":

                alerts.append({

                    "system": item["system"],

                    "alert": "HIGH_LATENCY",

                    "status": "TRIGGERED"
                })

        return alerts
