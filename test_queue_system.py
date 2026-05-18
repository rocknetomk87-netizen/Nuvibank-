from infrastructure.queue.task_queue import (
    TaskQueue
)

from infrastructure.workers.worker_engine import (
    WorkerEngine
)

TaskQueue.add_task({

    "type": "TRANSFER",

    "from": "rock",

    "to": "alex",

    "amount": 5000
})

TaskQueue.add_task({

    "type": "FRAUD_CHECK",

    "user": "rock"
})

TaskQueue.add_task({

    "type": "NOTIFICATION",

    "message": "Transfer complete"
})

WorkerEngine.process()
