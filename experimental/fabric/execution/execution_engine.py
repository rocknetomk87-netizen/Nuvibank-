class ExecutionEngine:

    def execute(
        self,
        task,
        priority
    ):

        return {

            "task": task,

            "priority": priority,

            "status": "DONE"
        }
