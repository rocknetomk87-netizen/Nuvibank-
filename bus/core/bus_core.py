from bus.events.event_bus import (
    EventBus
)

from bus.context.context_engine import (
    ContextEngine
)

from bus.shared.shared_memory import (
    SharedMemory
)

class BusCore:

    def __init__(self):

        self.events = EventBus()

        self.context = (
            ContextEngine()
        )

        self.shared = (
            SharedMemory()
        )

    def process(self):

        self.events.publish(

            {
                "event": "FRAUD_ALERT"
            }
        )

        self.context.update(

            "risk",

            "HIGH"
        )

        self.shared.store(

            "SENTINEL_CORE",

            {
                "status": "THREAT"
            }
        )

        return {

            "events": (
                self.events.all_events()
            ),

            "context": (
                self.context.state()
            ),

            "shared": (
                self.shared.read_all()
            )
        }
