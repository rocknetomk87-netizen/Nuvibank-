import asyncio

class AsyncEventEngine:

    async def emit(self, event):

        await asyncio.sleep(1)

        return {
            "event": event,
            "status": "EMITTED"
        }
