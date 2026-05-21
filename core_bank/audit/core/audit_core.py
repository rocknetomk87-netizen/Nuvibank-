from audit.hash.hash_engine import (
    HashEngine
)

from audit.chain.chain_engine import (
    ChainEngine
)

from audit.storage.storage_engine import (
    StorageEngine
)

class AuditCore:

    def __init__(self):

        self.hash = (
            HashEngine()
        )

        self.chain = (
            ChainEngine()
        )

        self.storage = (
            StorageEngine()
        )

        self.previous_hash = (
            "GENESIS"
        )

    def log_event(

        self,

        event
    ):

        current_hash = (
            self.hash
            .generate(event)
        )

        chain_event = (
            self.chain
            .create_event(

                event,

                self.previous_hash,

                current_hash
            )
        )

        self.storage.store(
            chain_event
        )

        self.previous_hash = (
            current_hash
        )

    def logs(self):

        return (
            self.storage
            .all_logs()
        )
