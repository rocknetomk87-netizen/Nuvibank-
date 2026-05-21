class ClusterRecovery:

    def recover(self, failed_nodes):

        recovered = []

        for node in failed_nodes:

            recovered.append({

                "node": node["id"],

                "recovery": "FAILOVER_SWITCH",

                "status": "RECOVERED"
            })

        return recovered
