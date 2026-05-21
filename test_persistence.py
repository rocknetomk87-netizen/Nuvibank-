from persistence_db.core.persistence_core import (
    PersistenceCore
)

engine = PersistenceCore()

systems = [

    {
        "system": "EVENT_BUS",
        "health": "HEALTHY",
        "latency": 20
    },

    {
        "system": "QUEUE_SYSTEM",
        "health": "HEALTHY",
        "latency": 25
    },

    {
        "system": "WORKER_POOL",
        "health": "HEALTHY",
        "latency": 30
    }
]

result = engine.persist(
    systems
)

print(result)
