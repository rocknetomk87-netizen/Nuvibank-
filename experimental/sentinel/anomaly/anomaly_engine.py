class AnomalyEngine:

    def detect(

        self,

        events
    ):

        anomalies = []

        for event in events:

            if event["risk"] >= 8:

                anomalies.append(event)

        return anomalies
