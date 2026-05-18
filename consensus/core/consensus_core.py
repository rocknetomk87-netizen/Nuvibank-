from consensus.voting.voting_engine import (
    VotingEngine
)

from consensus.state.state_engine import (
    StateEngine
)

from consensus.sync.sync_engine import (
    SyncEngine
)

class ConsensusCore:

    def __init__(self):

        self.voting = VotingEngine()

        self.state = StateEngine()

        self.sync = SyncEngine()

    def execute(

        self,

        nodes,
        key,
        value
    ):

        approved = (
            self.voting.vote(nodes)
        )

        if not approved:

            return {

                "status": "REJECTED"
            }

        self.state.update(
            key,
            value
        )

        synced = (
            self.sync.sync(
                nodes,
                self.state.get_state()
            )
        )

        return {

            "status": "APPROVED",

            "state": self.state.get_state(),

            "sync": synced
        }
