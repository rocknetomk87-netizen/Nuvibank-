class AnomalyDetector:

    @staticmethod
    def detect(user_profile, transaction):

        avg = user_profile["avg_transfer"]

        amount = transaction["amount"]

        if amount > avg * 5:

            return True

        return False
