from quantum.anticipation.anticipation_core import (
    AnticipationCore
)

core = AnticipationCore()

result = core.execute({

    "avg_transfer": 5000,

    "daily_login": True
})

print(result)
