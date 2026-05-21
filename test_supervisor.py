from supervisor.core.supervisor_core import (
    SupervisorCore
)

supervisor = SupervisorCore()

systems = [

    {
        "name": "QUEUE_SYSTEM",
        "status": "RUNNING"
    },

    {
        "name": "ASYNC_RUNTIME",
        "status": "RUNNING"
    },

    {
        "name": "WORKER_POOL",
        "status": "FAILED"
    }
]

result = supervisor.supervise(
    systems
)

print(result)
