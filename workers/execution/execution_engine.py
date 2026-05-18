class ExecutionEngine:

    def execute(self, workers):

        results = []

        for worker in workers:

            results.append({
                "worker": worker["worker"],
                "task": worker["task"]["task"],
                "status": "DONE"
            })

        return results
