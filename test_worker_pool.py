from worker_pool.core.worker_pool_core import (
    WorkerPoolCore
)

pool = WorkerPoolCore()

tasks = [

    {
        "task": "fraud_scan"
    },

    {
        "task": "wallet_validation"
    },

    {
        "task": "user_sync"
    },

    {
        "task": "security_audit"
    }
]

result = pool.process(tasks)

print(result)
