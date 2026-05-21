from worker_pool.workers.worker_engine import (
    WorkerEngine
)

from worker_pool.balance.load_balancer import (
    LoadBalancer
)

from worker_pool.runtime.pool_runtime import (
    PoolRuntime
)


class WorkerPoolCore:

    def __init__(self):

        self.workers = [

            WorkerEngine("worker-1"),

            WorkerEngine("worker-2"),

            WorkerEngine("worker-3")
        ]

        self.balancer = LoadBalancer()

        self.runtime = PoolRuntime()

    def process(self, tasks):

        distributed = self.balancer.distribute(
            tasks,
            self.workers
        )

        runtime = self.runtime.status()

        return {
            "distributed_tasks": distributed,
            "runtime": runtime
        }
