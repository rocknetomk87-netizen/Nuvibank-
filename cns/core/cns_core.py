from cns.monitor.system_monitor import (
    SystemMonitor
)

from cns.decision.decision_engine import (
    CNSDecisionEngine
)

from cns.recovery.recovery_engine import (
    RecoveryEngine
)

from cns.intelligence.intelligence_core import (
    IntelligenceCore
)

class CNSCore:

    @staticmethod
    def run():

        state = SystemMonitor.get_state()

        print(
            "[SYSTEM STATE]",
            state
        )

        decisions = CNSDecisionEngine.analyze(
            state
        )

        print(
            "[DECISIONS]",
            decisions
        )

        for decision in decisions:

            RecoveryEngine.recover(
                decision
            )

        optimization = IntelligenceCore.optimize()

        print(
            "[OPTIMIZATION]",
            optimization
        )
