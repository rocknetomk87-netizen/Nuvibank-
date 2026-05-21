class SyncEngine:

    def synchronize(self):

        modules = [
            "DNA_CORE",
            "RUNTIME_CORE",
            "SENTINEL_CORE",
            "CONSENSUS_CORE",
            "WORKER_CORE",
            "MASTER_CORE",
            "LIVE_CORE"
        ]

        return {
            "synced": True,
            "modules": modules
        }
