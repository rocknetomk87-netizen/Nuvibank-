from datetime import datetime

class SnapshotEngine:

    def snapshot(self, system):

        return {
            "snapshot": True,
            "timestamp": str(datetime.utcnow()),
            "system": system
        }
