class WorkerEngine:

    def execute(self, task):

        return {
            "worker": "ACTIVE",
            "task": task,
            "execution": "SUCCESS"
        }
