class PatternEngine:

    @staticmethod
    def detect(profile, transaction):

        alerts = []

        if transaction["amount"] > (
            profile["avg_transfer"] * 3
        ):

            alerts.append(
                "ABNORMAL_AMOUNT"
            )

        if transaction.get(
            "new_device",
            False
        ):

            alerts.append(
                "NEW_DEVICE"
            )

        return alerts
