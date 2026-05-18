from infra.state.state_engine import (
    StateEngine
)

from infra.health.health_engine import (
    HealthEngine
)

from infra.monitor.monitor_engine import (
    MonitorEngine
)

class InfraCore:

    def __init__(self):

        self.state = StateEngine()

        self.health = HealthEngine()

        self.monitor = MonitorEngine()

    def infrastructure(self):

        return {

            "state": (
                self.state.global_state()
            ),

            "health": (
                self.health.health()
            ),

            "monitor": (
                self.monitor.monitor()
            )
        }
