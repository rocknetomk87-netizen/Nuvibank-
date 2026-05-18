from runtime.events.event_loop import EventLoop
from runtime.state.state_manager import StateManager
from runtime.streams.stream_engine import StreamEngine
from runtime.execution.runtime_executor import RuntimeExecutor


class RuntimeCore:
    def __init__(self):
        self.loop = EventLoop()
        self.state = StateManager()
        self.stream = StreamEngine()
        self.executor = RuntimeExecutor()

    def run(self):
        event = {
            "type": "FRAUD_ALERT",
            "risk": "HIGH"
        }

        self.loop.publish(event)

        current = self.loop.consume()

        streamed = self.stream.process(current)

        executed = self.executor.execute("LOCKDOWN")

        self.state.update("last_event", current)

        return {
            "event": current,
            "stream": streamed,
            "execution": executed,
            "state": self.state.get()
        }
