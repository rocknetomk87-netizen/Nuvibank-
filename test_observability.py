from observability.metrics.metrics_engine import (
    MetricsEngine
)

from observability.health.health_engine import (
    HealthEngine
)

from observability.logs.log_engine import (
    LogEngine
)

MetricsEngine.increment(
    "requests"
)

MetricsEngine.increment(
    "transfers"
)

MetricsEngine.increment(
    "fraud_alerts"
)

print(

    MetricsEngine.get_metrics()
)

status = HealthEngine.node_status(

    "NODE-1",

    40,

    50
)

print(status)

LogEngine.log(

    "TRANSFER",

    {

        "from": "rock",

        "to": "alex",

        "amount": 5000
    }
)

print(

    LogEngine.get_logs()
)
