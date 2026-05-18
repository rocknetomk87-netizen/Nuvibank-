from scaling.workers.worker_manager import (
    WorkerManager
)

from scaling.balance.load_balancer import (
    LoadBalancer
)

class AdaptiveScaler:

    @staticmethod
    def analyze(load):

        status = LoadBalancer.distribute(
            load
        )

        print(
            "[LOAD STATUS]",
            status
        )

        if status == "HIGH_LOAD":

            WorkerManager.scale_up()

        elif status == "NORMAL_LOAD":

            WorkerManager.scale_down()

        return WorkerManager.get_workers()
