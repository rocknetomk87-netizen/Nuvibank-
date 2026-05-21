class LoadBalancer:

    def distribute(self, tasks, workers):

        distributed = []

        total_workers = len(workers)

        for index, task in enumerate(tasks):

            worker = workers[
                index % total_workers
            ]

            distributed.append(
                worker.execute(task)
            )

        return distributed
