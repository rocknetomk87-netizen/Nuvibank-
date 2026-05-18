import asyncio

class AsyncRuntime:

    async def runtime(self):

        await asyncio.sleep(1)

        return {
            "runtime": "ASYNC_RUNTIME",
            "status": "ACTIVE"
        }
