from governance.rules.rule_engine import (
    RuleEngine
)

from governance.priorities.priority_engine import (
    PriorityEngine
)

from governance.decisions.decision_engine import (
    DecisionEngine
)

class GovernanceCore:

    def __init__(self):

        self.rules = (
            RuleEngine()
        )

        self.priority = (
            PriorityEngine()
        )

        self.decisions = (
            DecisionEngine()
        )

    def process(

        self,

        event,
        risk,
        load
    ):

        rule = (
            self.rules
            .validate(event)
        )

        priority = (
            self.priority
            .get_priority(event)
        )

        decisions = (
            self.decisions
            .decide(
                risk,
                load
            )
        )

        return {

            "rule": rule,

            "priority": priority,

            "decisions": decisions
        }
