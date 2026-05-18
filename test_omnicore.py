from omnicore.core.omnicore import OmniCore


core = OmniCore()

event = {
    "type": "FRAUD_ALERT",
    "risk": "HIGH",
    "user": "rock"
}

result = core.run(event)

print(result)
