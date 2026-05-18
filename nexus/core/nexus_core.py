from nexus.control.control_engine import (
    ControlEngine
)

from nexus.sync.sync_engine import (
    SyncEngine
)

from nexus.state.state_engine import (
    NexusState
)

class NexusCore:

    def __init__(self):

        self.control = (
            ControlEngine()
        )

        self.sync = (
            SyncEngine()
        )

        self.state = (
            NexusState()
        )

    def nexus(self):

        return {

            "control": (
                self.control.control()
            ),

            "sync": (
                self.sync.sync()
            ),

            "state": (
                self.state.global_state()
            )
        }
