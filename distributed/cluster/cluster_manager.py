from distributed.nodes.node_engine import (
    NodeEngine
)

class ClusterManager:

    @staticmethod
    def create_cluster():

        return [

            NodeEngine(
                "NODE-1",
                2
            ),

            NodeEngine(
                "NODE-2",
                2
            ),

            NodeEngine(
                "NODE-3",
                2
            )
        ]
