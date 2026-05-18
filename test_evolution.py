from evolution.adaptive.evolution_core import (
    EvolutionCore
)

core = EvolutionCore()

result = core.evolve({

    "cpu": 90,

    "fraud_alerts": 8
})

print(result)
