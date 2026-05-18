from security.fraud.fraud_engine import FraudEngine

from security.anomaly.anomaly_detector import (
    AnomalyDetector
)

class RiskEngine:

    @staticmethod
    def evaluate(
        user_profile,
        transaction
    ):

        anomaly = AnomalyDetector.detect(
            user_profile,
            transaction
        )

        fraud_result = FraudEngine.analyze(
            transaction
        )

        return {
            "anomaly": anomaly,
            "fraud": fraud_result
        }
