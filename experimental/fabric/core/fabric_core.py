from fabric.scheduler.scheduler_engine import (
    SchedulerEngine
)

from fabric.priority.priority_engine import (
    PriorityEngine
)

from fabric.execution.execution_engine import (
    ExecutionEngine
)

class FabricCore:

    def __init__(self):

        self.scheduler = (
            SchedulerEngine()
        )

        self.priority = (
            PriorityEngine()
        )

        self.execution = (
            ExecutionEngine()
        )

    def process(
        self,
        event
    ):

        scheduled = (
            self.scheduler.schedule(
                event
            )
        )

        priority = (
            self.priority.priority(
                event
            )
        )

        executed = (
            self.execution.execute(
                event,
                priority
            )
        )

        return {

            "scheduled": scheduled,

            "priority": priority,

            "executed": executed
        }
