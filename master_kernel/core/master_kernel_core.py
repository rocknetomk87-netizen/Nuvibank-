from master_kernel.orchestrator.orchestrator_engine import (
    OrchestratorEngine
)

from master_kernel.monitor.system_monitor import (
    SystemMonitor
)

from master_kernel.control.control_engine import (
    ControlEngine
)

from master_kernel.runtime.master_runtime import (
    MasterRuntime
)


class MasterKernelCore:

    def __init__(self):

        self.orchestrator = (
            OrchestratorEngine()
        )

        self.monitor = (
            SystemMonitor()
        )

        self.control = (
            ControlEngine()
        )

        self.runtime = (
            MasterRuntime()
        )

    def initialize(self):

        boot = self.orchestrator.boot()

        report = self.monitor.inspect(
            boot
        )

        control = self.control.manage(
            report
        )

        runtime = self.runtime.status()

        return {

            "boot": boot,

            "report": report,

            "control": control,

            "runtime": runtime
        }
