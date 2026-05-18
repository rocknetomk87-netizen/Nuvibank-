from neural.execution.execution_core import (
    ExecutionCore
)

core = ExecutionCore()

result = core.execute(

    {

        "type":
        "TRANSFER"
    },

    3,

    120
)

print(result)
