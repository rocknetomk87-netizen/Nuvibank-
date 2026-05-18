from persistence.state.state_storage import (
    StateStorage
)

from persistence.snapshots.snapshot_engine import (
    SnapshotEngine
)

from persistence.recovery.recovery_engine import (
    RecoveryEngine
)

class PersistenceCore:

    def __init__(self):

        self.storage = (
            StateStorage()
        )

        self.snapshot = (
            SnapshotEngine()
        )

        self.recovery = (
            RecoveryEngine()
        )

    def persist(self):

        data = {

            "system": "NUVIBANK™",

            "security": "MAXIMUM",

            "nodes": 3
        }

        snap = (
            self.snapshot.snapshot(
                data
            )
        )

        self.storage.save(

            "nuvibank_state.json",

            snap
        )

        loaded = (
            self.storage.load(
                "nuvibank_state.json"
            )
        )

        recovered = (
            self.recovery.recover(
                loaded
            )
        )

        return recovered
