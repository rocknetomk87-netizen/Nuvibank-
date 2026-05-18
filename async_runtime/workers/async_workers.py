import asyncio

class AsyncWorkers:

    async def process(self, task):

        await asyncio.sleep(1)

        return {
            "worker": "WORKER_ASYNC",
            "task": task,
            "status": "PROCESSED"
        }
