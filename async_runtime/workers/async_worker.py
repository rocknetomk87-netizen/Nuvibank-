import asyncio

from async_runtime.tasks.async_task_engine import (
    AsyncTaskEngine
)


class AsyncWorker:

    def __init__(self):

        self.engine = AsyncTaskEngine()

    async def run_tasks(self, tasks):

        executions = [

            self.engine.execute(
                task["task"],
                task.get("delay", 1)
            )

            for task in tasks
        ]

        results = await asyncio.gather(
            *executions
        )

        return results
