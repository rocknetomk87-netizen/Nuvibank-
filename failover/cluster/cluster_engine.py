class ClusterEngine:

    def distribute(self, active_nodes):

        distribution = []

        tasks = [

            "fraud_scan",

            "wallet_sync",

            "security_audit",

            "analytics"
        ]

        index = 0

        for task in tasks:

            node = active_nodes[
                index % len(active_nodes)
            ]

            distribution.append({

                "task": task,

                "node": node["id"],

                "status": "ASSIGNED"
            })

            index += 1

        return distribution
