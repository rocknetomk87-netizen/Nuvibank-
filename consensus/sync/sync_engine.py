class SyncEngine:

    def sync(

        self,

        nodes,
        state
    ):

        synced = []

        for node in nodes:

            synced.append({

                "node": node["id"],

                "synced": True,

                "state": state
            })

        return synced
