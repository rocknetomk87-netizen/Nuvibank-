from orchestration.events.event_engine import (
    EventEngine
)

from orchestration.router.router_engine import (
    RouterEngine
)

from orchestration.execution.execution_engine import (
    ExecutionEngine
)

class OrchestrationCore:

    def __init__(self):

        self.events = EventEngine()

        self.router = RouterEngine()

        self.execution = (
            ExecutionEngine()
        )

    def process(
        self,
        event,
        payload
    ):

        created = (
            self.events.create_event(
                event,
                payload
            )
        )

        route = (
            self.router.route(event)
        )

        executed = (
            self.execution.execute(
                route
            )
        )

        return {

            "created": created,

            "route": route,

            "executed": executed
        }
