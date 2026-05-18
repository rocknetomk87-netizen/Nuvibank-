from selfheal.recovery.recovery_engine import (
    RecoveryEngine
)

from selfheal.repair.repair_engine import (
    RepairEngine
)

from selfheal.restart.restart_engine import (
    RestartEngine
)

class SelfHealCore:

    def __init__(self):

        self.recovery = (
            RecoveryEngine()
        )

        self.repair = (
            RepairEngine()
        )

        self.restart_engine = (
            RestartEngine()
        )

    def heal(self):

        recovery = (
            self.recovery
            .recover("PAYMENT_API")
        )

        repair = (
            self.repair
            .repair("NODE-2")
        )

        restart = (
            self.restart_engine
            .restart("WORKER-7")
        )

        return {

            "recovery":
            recovery,

            "repair":
            repair,

            "restart":
            restart
        }
