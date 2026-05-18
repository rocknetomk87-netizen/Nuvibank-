from distributed.cache.cache_engine import (
    CacheEngine
)

from distributed.memory.memory_engine import (
    DistributedMemory
)

from distributed.sync.sync_engine import (
    SyncEngine
)

CacheEngine.set(

    "session_rock",

    {

        "user": "rock"
    }
)

print(

    CacheEngine.get(
        "session_rock"
    )
)

DistributedMemory.store(

    "risk_score",

    85
)

print(

    DistributedMemory.retrieve(
        "risk_score"
    )
)

SyncEngine.synchronize(

    "NODE-1",

    "NODE-2",

    {

        "balance": 5000
    }
)
