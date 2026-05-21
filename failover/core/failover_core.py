from failover.nodes.node_engine import (
    NodeEngine
)

from failover.recovery.recovery_engine import (
    ClusterRecovery
)

from failover.cluster.cluster_engine import (
    ClusterEngine
)

from failover.runtime.failover_runtime import (
    FailoverRuntime
)


class FailoverCore:

    def __init__(self):

        self.nodes = NodeEngine()

        self.recovery = ClusterRecovery()

        self.cluster = ClusterEngine()

        self.runtime = FailoverRuntime()

    def execute(self, nodes):

        validated = self.nodes.validate(
            nodes
        )

        recovered = self.recovery.recover(
            validated["failed"]
        )

        distribution = self.cluster.distribute(
            validated["active"]
        )

        runtime = self.runtime.status()

        return {

            "cluster": distribution,

            "recovered": recovered,

            "runtime": runtime
        }
