from selfheal.core.selfheal_core import (
    SelfHealCore
)

selfheal = SelfHealCore()

failures = [

    "WORKER_POOL",

    "ASYNC_RUNTIME",

    "QUEUE_SYSTEM"
]

result = selfheal.heal(
    failures
)

print(result)
