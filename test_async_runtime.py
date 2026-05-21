import asyncio

from async_runtime.core.async_core import (
    AsyncCore
)


async def main():

    runtime = AsyncCore()

    tasks = [

        {
            "task": "fraud_scan",
            "delay": 1
        },

        {
            "task": "wallet_sync",
            "delay": 2
        },

        {
            "task": "security_audit",
            "delay": 1
        }
    ]

    result = await runtime.execute(tasks)

    print(result)


asyncio.run(main())
