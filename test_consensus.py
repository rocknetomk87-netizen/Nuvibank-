from consensus.core.consensus_core import (
    ConsensusCore
)

nodes = [

    {
        "id": "NODE-1",
        "status": "ONLINE"
    },

    {
        "id": "NODE-2",
        "status": "ONLINE"
    },

    {
        "id": "NODE-3",
        "status": "OFFLINE"
    }
]

core = ConsensusCore()

result = core.execute(

    nodes,

    "transaction",

    "APPROVED_5000"
)

print(result)
