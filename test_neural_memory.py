from neural_memory.core.neural_core import (
    NeuralCore
)

engine = NeuralCore()

decisions = [

    {
        "system": "WORKER_POOL",
        "decision": "REDISTRIBUTE_LOAD"
    },

    {
        "system": "ASYNC_RUNTIME",
        "decision": "KEEP_RUNNING"
    },

    {
        "system": "QUEUE_SYSTEM",
        "decision": "REDISTRIBUTE_LOAD"
    }
]

result = engine.process(
    decisions
)

print(result)
