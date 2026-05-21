class MonitorEngine:

    def classify(

        self,

        anomalies
    ):

        if len(anomalies) > 0:

            return {

                "status": "THREAT",

                "action": "LOCKDOWN"
            }

        return {

            "status": "SAFE"
        }
