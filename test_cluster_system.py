from distributed.cluster.cluster_manager import (
    ClusterManager
)

from distributed.router.task_router import (
    TaskRouter
)

nodes = ClusterManager.create_cluster()

tasks = [

    {"type": "TRANSFER"},

    {"type": "FRAUD_CHECK"},

    {"type": "LOGIN"},

    {"type": "NOTIFICATION"},

    {"type": "AUDIT"},

    {"type": "AI_ANALYSIS"}
]

for task in tasks:

    result = TaskRouter.route(
        nodes,
        task
    )

    print(

        "ROUTED TO:",

        result
    )
