from replication.state.state_engine import (
    StateEngine
)

from replication.sync.sync_engine import (
    SyncEngine
)

from replication.storage.storage_engine import (
    StorageEngine
)

from replication.runtime.replication_runtime import (
    ReplicationRuntime
)


class ReplicationCore:

    def __init__(self):

        self.state = StateEngine()

        self.sync = SyncEngine()

        self.storage = StorageEngine()

        self.runtime = ReplicationRuntime()

    def execute(self, nodes):

        state = self.state.create_state()

        sync = self.sync.synchronize(
            nodes,
            state
        )

        storage = self.storage.persist(
            state
        )

        runtime = self.runtime.status()

        return {

            "state": state,

            "replication": sync,

            "storage": storage,

            "runtime": runtime
        }
