from event_bus.events.event_engine import EventEngine
from event_bus.handlers.event_handler import EventHandler
from event_bus.runtime.event_runtime import EventRuntime


class EventBusCore:

    def __init__(self):

        self.engine = EventEngine()

        self.handler = EventHandler()

        self.runtime = EventRuntime()

    def dispatch(self, event, payload):

        created = self.engine.create_event(
            event,
            payload
        )

        handled = self.handler.handle(
            created
        )

        runtime = self.runtime.runtime_status()

        return {
            "created": created,
            "handled": handled,
            "runtime": runtime
        }
