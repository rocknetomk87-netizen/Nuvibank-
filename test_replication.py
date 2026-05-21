from replication.core.replication_core import (
    ReplicationCore
)

replication = ReplicationCore()

nodes = [

    "node-1",

    "node-2",

    "node-3"
]

result = replication.execute(
    nodes
)

print(result)
