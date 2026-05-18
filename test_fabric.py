from fabric.core.fabric_core import (
    FabricCore
)

core = FabricCore()

result = core.process(
    "FRAUD"
)

print(result)
