from neural.priority.priority_engine import (
    PriorityEngine
)

from neural.throughput.throughput_engine import (
    ThroughputEngine
)

class ExecutionCore:

    def __init__(self):

        self.priority = PriorityEngine()

        self.throughput = ThroughputEngine()

    def execute(

        self,

        task,

        workers,

        queue
    ):

        priority = (
            self.priority
            .calculate_priority(
                task
            )
        )

        optimized = (
            self.throughput
            .optimize(
                workers,
                queue
            )
        )

        return {

            "priority":
            priority,

            "workers":
            optimized
        }
