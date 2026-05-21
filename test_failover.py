from failover.core.failover_core import (
    FailoverCore
)

cluster = FailoverCore()

nodes = [

    {
        "id": "node-1",
        "status": "ONLINE"
    },

    {
        "id": "node-2",
        "status": "ONLINE"
    },

    {
        "id": "node-3",
        "status": "OFFLINE"
    }
]

result = cluster.execute(
    nodes
)

print(result)
