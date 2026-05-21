import asyncio


class AsyncTaskEngine:

    async def execute(
        self,
        name,
        delay=1
    ):

        await asyncio.sleep(delay)

        return {
            "task": name,
            "delay": delay,
            "status": "COMPLETED"
        }
