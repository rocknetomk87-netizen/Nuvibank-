from datetime import datetime

class SnapshotEngine:

    def snapshot(
        self,
        system
    ):

        return {

            "timestamp":
            str(datetime.now()),

            "system": system,

            "status": "SNAPSHOT_CREATED"
        }
