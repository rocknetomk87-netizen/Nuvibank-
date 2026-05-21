from supervisor.monitor.system_monitor import (
    SystemMonitor
)

from supervisor.recovery.recovery_engine import (
    RecoveryEngine
)

from supervisor.runtime.supervisor_runtime import (
    SupervisorRuntime
)


class SupervisorCore:

    def __init__(self):

        self.monitor = SystemMonitor()

        self.recovery = RecoveryEngine()

        self.runtime = SupervisorRuntime()

    def supervise(self, systems):

        report = self.monitor.inspect(
            systems
        )

        recoveries = self.recovery.recover(
            report
        )

        runtime = self.runtime.status()

        return {

            "report": report,

            "recoveries": recoveries,

            "runtime": runtime
        }
