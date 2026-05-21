class StorageEngine:

    def persist(
        self,
        db,
        systems
    ):

        for system in systems:

            db.insert_state(

                system["system"],

                system["health"],

                system["latency"]
            )

        return {

            "storage": "PERSISTED",

            "records": len(systems)
        }
