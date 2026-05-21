class ThroughputEngine:

    def optimize(

        self,

        active_workers,

        queue_size
    ):

        if queue_size > 100:

            return active_workers + 2

        if queue_size > 50:

            return active_workers + 1

        if queue_size < 10:

            return max(
                1,
                active_workers - 1
            )

        return active_workers
