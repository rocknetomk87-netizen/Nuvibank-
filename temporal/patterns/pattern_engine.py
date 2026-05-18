class PatternEngine:

    def detect_patterns(

        self,

        events
    ):

        fraud_hours = []

        for event in events:

            if event["event"] == "FRAUD":

                fraud_hours.append(
                    event["hour"]
                )

        return {

            "fraud_hours": fraud_hours
        }
