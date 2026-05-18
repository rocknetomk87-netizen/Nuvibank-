class MetricsEngine:

    metrics = {

        "requests": 0,

        "transfers": 0,

        "fraud_alerts": 0,

        "failed_requests": 0
    }

    @classmethod
    def increment(

        cls,

        metric
    ):

        if metric in cls.metrics:

            cls.metrics[metric] += 1

    @classmethod
    def get_metrics(cls):

        return cls.metrics
