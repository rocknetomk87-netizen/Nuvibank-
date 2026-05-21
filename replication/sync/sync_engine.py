class SyncEngine:

    def synchronize(self, nodes, state):

        replicated = []

        for node in nodes:

            replicated.append({

                "node": node,

                "state": state,

                "sync": "COMPLETED"
            })

        return replicated
