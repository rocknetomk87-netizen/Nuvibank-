import asyncio

from async.core.async_core import AsyncCore

core = AsyncCore()

result = asyncio.run(
    core.execute()
)

print(result)
