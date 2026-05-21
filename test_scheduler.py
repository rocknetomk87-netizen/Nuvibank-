from scheduler.core.scheduler_core import (
    SchedulerCore
)

scheduler = SchedulerCore()

tasks = [
    {
        "task": "analytics",
        "priority": "LOW"
    },

    {
        "task": "fraud_detection",
        "priority": "HIGH"
    },

    {
        "task": "user_sync",
        "priority": "NORMAL"
    }
]

result = scheduler.organize(tasks)

print(result)
