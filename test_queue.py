from queue.core.queue_core import QueueCore


queue = QueueCore()

result = queue.dispatch(
    "TRANSFER_VALIDATION",
    {
        "amount": 5000,
        "currency": "USD"
    },
    priority="HIGH"
)

print(result)
