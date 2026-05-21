from queue.tasks.task_engine import TaskEngine
from queue.workers.worker_engine import WorkerEngine
from queue.runtime.queue_runtime import QueueRuntime


class QueueCore:

    def __init__(self):

        self.tasks = TaskEngine()

        self.workers = WorkerEngine()

        self.runtime = QueueRuntime()

    def dispatch(
        self,
        name,
        payload,
        priority="NORMAL"
    ):

        task = self.tasks.create_task(
            name,
            payload,
            priority
        )

        execution = self.workers.execute(
            task
        )

        runtime = self.runtime.status()

        return {
            "task": task,
            "execution": execution,
            "runtime": runtime
        }
