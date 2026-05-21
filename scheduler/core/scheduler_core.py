from scheduler.priority.priority_engine import (
    PriorityEngine
)

from scheduler.runtime.scheduler_runtime import (
    SchedulerRuntime
)


class SchedulerCore:

    def __init__(self):

        self.priority = PriorityEngine()

        self.runtime = SchedulerRuntime()

    def organize(self, tasks):

        ordered = self.priority.sort_tasks(
            tasks
        )

        runtime = self.runtime.status()

        return {
            "ordered_tasks": ordered,
            "runtime": runtime
        }
