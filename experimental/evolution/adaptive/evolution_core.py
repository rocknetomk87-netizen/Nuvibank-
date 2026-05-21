from evolution.learning.learning_engine import (
    LearningEngine
)

from evolution.optimizer.optimizer_engine import (
    OptimizerEngine
)

class EvolutionCore:

    def __init__(self):

        self.learning = (
            LearningEngine()
        )

        self.optimizer = (
            OptimizerEngine()
        )

    def evolve(

        self,

        metrics
    ):

        knowledge = (
            self.learning.learn(
                metrics
            )
        )

        actions = (
            self.optimizer.optimize(
                knowledge
            )
        )

        return {

            "knowledge":
            knowledge,

            "actions":
            actions
        }
