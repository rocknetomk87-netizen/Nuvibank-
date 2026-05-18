from memory.history.history_engine import (
    HistoryEngine
)

from memory.events.event_memory import (
    EventMemory
)

from memory.patterns.pattern_memory import (
    PatternMemory
)

class MemoryCore:

    def __init__(self):

        self.history = (
            HistoryEngine()
        )

        self.events = (
            EventMemory()
        )

        self.patterns = (
            PatternMemory()
        )

    def learn(self):

        self.history.store(
            "FAILED_LOGIN"
        )

        self.history.store(
            "FAILED_LOGIN"
        )

        self.history.store(
            "FAILED_LOGIN"
        )

        self.history.store(
            "FAILED_LOGIN"
        )

        all_events = (
            self.history.get_all()
        )

        detected = (
            self.patterns
            .detect(all_events)
        )

        memory = (
            self.events
            .remember(
                detected
            )
        )

        return {

            "events":
            all_events,

            "patterns":
            detected,

            "memory":
            memory
        }
