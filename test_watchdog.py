from watchdog.core.watchdog_core import (
    WatchdogCore
)

watchdog = WatchdogCore()

systems = [

    {
        "name": "QUEUE_SYSTEM",
        "latency": 20
    },

    {
        "name": "ASYNC_RUNTIME",
        "latency": 40
    },

    {
        "name": "WORKER_POOL",
        "latency": 250
    }
]

result = watchdog.monitor(
    systems
)

print(result)
