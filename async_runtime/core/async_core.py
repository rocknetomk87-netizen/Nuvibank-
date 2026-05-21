from async_runtime.workers.async_worker import (
    AsyncWorker
)

from async_runtime.runtime.async_runtime import (
    AsyncRuntime
)


class AsyncCore:

    def __init__(self):

        self.worker = AsyncWorker()

        self.runtime = AsyncRuntime()

    async def execute(self, tasks):

        results = await self.worker.run_tasks(
            tasks
        )

        runtime = self.runtime.status()

        return {
            "results": results,
            "runtime": runtime
        }
