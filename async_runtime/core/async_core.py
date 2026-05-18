import asyncio

from async.events.async_event_engine import AsyncEventEngine
from async.queue.async_queue import AsyncQueue
from async.workers.async_workers import AsyncWorkers
from async.runtime.async_runtime import AsyncRuntime

class AsyncCore:

    def __init__(self):

        self.events = AsyncEventEngine()

        self.queue = AsyncQueue()

        self.workers = AsyncWorkers()

        self.runtime = AsyncRuntime()

    async def execute(self):

        event = await self.events.emit(
            "FRAUD_ALERT"
        )

        queued = await self.queue.enqueue(
            event
        )

        worker = await self.workers.process(
            queued
        )

        runtime = await self.runtime.runtime()

        return {
            "event": event,
            "queue": queued,
            "worker": worker,
            "runtime": runtime
        }
