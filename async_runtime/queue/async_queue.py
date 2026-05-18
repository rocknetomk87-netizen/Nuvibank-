import asyncio

class AsyncQueue:

    async def enqueue(self, payload):

        await asyncio.sleep(1)

        return {
            "queued": True,
            "payload": payload
        }
