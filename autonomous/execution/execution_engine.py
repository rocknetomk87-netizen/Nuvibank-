class ExecutionEngine:

    def dispatch(

        self,

        tasks
    ):

        executed = []

        for task in tasks:

            executed.append({

                "task": task,

                "result": "DONE"
            })

        return executed
