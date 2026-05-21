from persistence_db.database.db_engine import (
    DatabaseEngine
)

from persistence_db.storage.storage_engine import (
    StorageEngine
)

from persistence_db.runtime.runtime_engine import (
    RuntimeEngine
)


class PersistenceCore:

    def __init__(self):

        self.db = DatabaseEngine()

        self.storage = StorageEngine()

        self.runtime = RuntimeEngine()

        self.db.initialize()

    def persist(self, systems):

        persisted = self.storage.persist(

            self.db,
            systems
        )

        data = self.db.fetch_all()

        runtime = self.runtime.status()

        return {

            "persisted": persisted,

            "data": data,

            "runtime": runtime
        }
