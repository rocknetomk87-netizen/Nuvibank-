from master.boot.boot_engine import BootEngine
from master.security.security_engine import SecurityEngine
from master.runtime.runtime_manager import RuntimeManager
from master.state.state_manager import StateManager


class MasterCore:

    def __init__(self):

        self.boot_engine = BootEngine()
        self.security_engine = SecurityEngine()
        self.runtime_manager = RuntimeManager()
        self.state_manager = StateManager()

    def initialize(self):

        return {

            "boot": self.boot_engine.boot(),

            "security":
            self.security_engine.security_status(),

            "runtime":
            self.runtime_manager.runtime_status(),

            "state":
            self.state_manager.system_state()
        }
