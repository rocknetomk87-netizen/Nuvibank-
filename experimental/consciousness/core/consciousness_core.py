from consciousness.state.state_engine import (
    StateEngine
)

from consciousness.awareness.awareness_engine import (
    AwarenessEngine
)

from consciousness.decision.decision_engine import (
    DecisionEngine
)

class ConsciousnessCore:

    def __init__(self):

        self.state = StateEngine()

        self.awareness = AwarenessEngine()

        self.decision = DecisionEngine()

    def think(self):

        state = (
            self.state.load_state()
        )

        awareness = (
            self.awareness.analyze(
                state
            )
        )

        decisions = (
            self.decision.decide(
                awareness
            )
        )

        return {

            "state": state,

            "awareness": awareness,

            "decisions": decisions
        }
