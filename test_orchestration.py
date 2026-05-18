from orchestration.core.orchestration_core import (
    OrchestrationCore
)

core = OrchestrationCore()

result = core.process(

    "FRAUD",

    {
        "user": "rock",
        "amount": 5000
    }
)

print(result)
