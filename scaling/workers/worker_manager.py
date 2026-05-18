class WorkerManager:

    workers = 3

    @classmethod
    def scale_up(cls):

        cls.workers += 1

        print(
            "[SCALE UP]",
            cls.workers
        )

    @classmethod
    def scale_down(cls):

        if cls.workers > 1:

            cls.workers -= 1

        print(
            "[SCALE DOWN]",
            cls.workers
        )

    @classmethod
    def get_workers(cls):

        return cls.workers
