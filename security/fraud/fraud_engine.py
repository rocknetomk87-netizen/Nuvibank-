class FraudEngine:

    @staticmethod
    def analyze(transaction):

        amount = transaction["amount"]

        risk_score = 0

        if amount > 100000:

            risk_score += 80

        elif amount > 50000:

            risk_score += 40

        velocity = transaction.get(
            "velocity",
            1
        )

        if velocity > 5:

            risk_score += 30

        new_device = transaction.get(
            "new_device",
            False
        )

        if new_device:

            risk_score += 20

        if risk_score >= 80:

            return {
                "action": "BLOCK",
                "risk": risk_score
            }

        elif risk_score >= 50:

            return {
                "action": "MFA",
                "risk": risk_score
            }

        return {
            "action": "ALLOW",
            "risk": risk_score
        }
