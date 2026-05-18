class TaskQueue:

    queue = []

    @classmethod
    def add_task(
        cls,
        task
    ):

        cls.queue.append(task)

    @classmethod
    def get_task(cls):

        if len(cls.queue) == 0:

            return None

        return cls.queue.pop(0)
