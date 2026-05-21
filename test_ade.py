from ade.core.ade_core import ADECore

engine = ADECore()

metrics = [

    {
        "system": "WORKER_POOL",
        "latency": 250
    },

    {
        "system": "ASYNC_RUNTIME",
        "latency": 40
    },

    {
        "system": "QUEUE_SYSTEM",
        "latency": 180
    }
]

result = engine.execute(
    metrics
)

print(result)
