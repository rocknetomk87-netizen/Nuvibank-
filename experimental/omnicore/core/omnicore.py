from omnicore.control.control_engine import ControlEngine
from omnicore.sync.sync_engine import SyncEngine
from omnicore.intelligence.intelligence_engine import IntelligenceEngine
from omnicore.execution.execution_engine import ExecutionEngine
from omnicore.supervision.supervision_engine import SupervisionEngine


class OmniCore:

    def __init__(self):

        self.control = ControlEngine()
        self.sync = SyncEngine()
        self.intelligence = IntelligenceEngine()
        self.execution = ExecutionEngine()
        self.supervision = SupervisionEngine()

    def run(self, event):

        control = self.control.activate()

        sync = self.sync.synchronize()

        intelligence = self.intelligence.analyze(event)

        execution = self.execution.execute(
            intelligence["decision"]
        )

        supervision = self.supervision.monitor()

        return {
            "control": control,
            "sync": sync,
            "intelligence": intelligence,
            "execution": execution,
            "supervision": supervision
        }
