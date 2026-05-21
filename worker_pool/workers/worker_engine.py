class WorkerEngine:

    def __init__(self, worker_id):

        self.worker_id = worker_id

    def execute(self, task):

        return {
            "worker_id": self.worker_id,
            "task": task,
            "status": "EXECUTED"
        }
