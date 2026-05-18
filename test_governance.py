from governance.core.governance_core import (
    GovernanceCore
)

core = GovernanceCore()

result = core.process(

    event="FRAUD",

    risk=10,

    load=9
)

print(result)
