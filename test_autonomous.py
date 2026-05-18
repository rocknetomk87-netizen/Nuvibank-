from autonomous.core.autonomous_core import (
    AutonomousCore
)

core = AutonomousCore()

result = core.react(
    "FRAUD"
)

print(result)
