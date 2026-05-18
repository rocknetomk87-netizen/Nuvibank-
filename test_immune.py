from immune.core.immune_core import ImmuneCore

core = ImmuneCore()

result = core.defend({
    "ip": "192.168.1.10",
    "threat_level": "HIGH",
    "attacks": 12,
    "locations": 5
})

print(result)
