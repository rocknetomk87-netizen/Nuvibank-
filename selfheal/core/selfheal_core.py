from selfheal.recovery.recovery_engine import (
    RecoveryEngine
)

from selfheal.restart.restart_engine import (
    RestartEngine
)

from selfheal.repair.repair_engine import (
    RepairEngine
)

from selfheal.runtime.selfheal_runtime import (
    SelfHealRuntime
)


class SelfHealCore:

    def __init__(self):

        self.recovery = RecoveryEngine()

        self.restart = RestartEngine()

        self.repair = RepairEngine()

        self.runtime = SelfHealRuntime()

    def heal(self, failures):

        recovery = self.recovery.recover(
            failures
        )

        restart = self.restart.restart(
            failures
        )

        repair = self.repair.repair(
            failures
        )

        runtime = self.runtime.status()

        return {

            "recovery": recovery,

            "restart": restart,

            "repair": repair,

            "runtime": runtime
        }
