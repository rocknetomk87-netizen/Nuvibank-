from security.risk.risk_engine import (
    RiskEngine
)

user_profile = {

    "avg_transfer": 5000

}

transaction = {

    "amount": 120000,

    "velocity": 8,

    "new_device": True

}

result = RiskEngine.evaluate(
    user_profile,
    transaction
)

print(result)
