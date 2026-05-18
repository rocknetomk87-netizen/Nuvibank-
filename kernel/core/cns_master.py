from kernel.priorities.priority_engine import (
    PriorityEngine
)

from kernel.survival.survival_mode import (
    SurvivalMode
)

from kernel.control.control_engine import (
    ControlEngine
)

from kernel.orchestration.orchestrator import (
    Orchestrator
)

class CNSMaster:

    def __init__(self):

        self.priority = (
            PriorityEngine()
        )

        self.survival = (
            SurvivalMode()
        )

        self.control = (
            ControlEngine()
        )

        self.orchestrator = (
            Orchestrator()
        )

    def think(self):

        event = "FRAUD"

        priority = (
            self.priority
            .get_priority(event)
        )

        route = (
            self.orchestrator
            .route(event)
        )

        survival = (
            self.survival
            .activate(priority)
        )

        optimization = (
            self.control
            .optimize(90)
        )

        return {

            "event": event,

            "priority": priority,

            "route": route,

            "survival": survival,

            "optimization":
            optimization
        }
