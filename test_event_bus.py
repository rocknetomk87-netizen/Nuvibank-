from event_bus.core.event_bus_core import EventBusCore


bus = EventBusCore()

result = bus.dispatch(
    "FRAUD_ALERT",
    {
        "risk": "HIGH",
        "user": "rock"
    }
)

print(result)
