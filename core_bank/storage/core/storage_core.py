from storage.database.database_engine import DatabaseEngine
from storage.cache.cache_engine import CacheEngine
from storage.history.history_engine import HistoryEngine
from storage.snapshots.snapshot_engine import SnapshotEngine

class StorageCore:

    def __init__(self):

        self.database = DatabaseEngine()

        self.cache = CacheEngine()

        self.history = HistoryEngine()

        self.snapshot = SnapshotEngine()

    def persist(self):

        data = {
            "event": "FRAUD_ALERT",
            "risk": "HIGH"
        }

        return {

            "database":
                self.database.save(data),

            "cache":
                self.cache.cache(data),

            "history":
                self.history.record(data),

            "snapshot":
                self.snapshot.snapshot("NUVIBANK™")
        }
