from ade.brain.brain_engine import (
    BrainEngine
)

from ade.decision.decision_engine import (
    DecisionEngine
)

from ade.learning.learning_engine import (
    LearningEngine
)

from ade.runtime.ade_runtime import (
    ADERuntime
)


class ADECore:

    def __init__(self):

        self.brain = BrainEngine()

        self.decision = DecisionEngine()

        self.learning = LearningEngine()

        self.runtime = ADERuntime()

    def execute(self, metrics):

        analyzed = self.brain.analyze(
            metrics
        )

        executed = self.decision.execute(
            analyzed
        )

        learned = self.learning.learn(
            analyzed
        )

        runtime = self.runtime.status()

        return {

            "analysis": analyzed,

            "execution": executed,

            "learning": learned,

            "runtime": runtime
        }
