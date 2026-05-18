from infrastructure.queue.task_queue import (
    TaskQueue
)

class WorkerEngine:

    @staticmethod
    def process():

        while True:

            task = TaskQueue.get_task()

            if not task:

                break

            print(

                "[PROCESSING]",

                task
            )
