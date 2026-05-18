from system.bus.event_bus import EventBus

from system.events.handlers import (
    transfer_handler,
    fraud_handler,
    login_handler
)

# subscrições

EventBus.subscribe(
    "TRANSFER",
    transfer_handler
)

EventBus.subscribe(
    "FRAUD",
    fraud_handler
)

EventBus.subscribe(
    "LOGIN",
    login_handler
)

# emissão de eventos

EventBus.emit(
    "LOGIN",
    {
        "user": "rock"
    }
)

EventBus.emit(
    "TRANSFER",
    {
        "from": "rock",
        "to": "alex",
        "amount": 5000
    }
)

EventBus.emit(
    "FRAUD",
    {
        "risk": "HIGH"
    }
)
