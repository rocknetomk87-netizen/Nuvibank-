class DispatchEngine:

    def dispatch(self, tasks):

        workers = []

        for index, task in enumerate(tasks):

            workers.append({
                "worker": f"WORKER_{index+1}",
                "task": task
            })

        return workers
