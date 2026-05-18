from ai.memory.memory_engine import (
    MemoryEngine
)

from ai.profile.profile_engine import (
    ProfileEngine
)

from ai.patterns.pattern_engine import (
    PatternEngine
)

MemoryEngine.remember(

    "rock",

    {
        "type": "TRANSFER",
        "amount": 5000,
        "location": "LUANDA",
        "device": "TECNO"
    }
)

MemoryEngine.remember(

    "rock",

    {
        "type": "TRANSFER",
        "amount": 7000,
        "location": "LUANDA",
        "device": "TECNO"
    }
)

events = MemoryEngine.get_memory(
    "rock"
)

profile = ProfileEngine.build(
    events
)

transaction = {

    "amount": 50000,

    "new_device": True
}

alerts = PatternEngine.detect(
    profile,
    transaction
)

print(profile)

print(alerts)
