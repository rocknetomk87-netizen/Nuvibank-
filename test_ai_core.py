from ai.behavior.behavior_engine import BehaviorProfile
from ai.trust_score import calculate_trust_score

profile = BehaviorProfile()

profile.register_login(20)
profile.register_transfer(1500)
profile.register_device("TECNO_KM4")
profile.register_location("Luanda")

data = profile.analyze_behavior()

score = calculate_trust_score(data)

print(data)
print("Trust Score:", score)
