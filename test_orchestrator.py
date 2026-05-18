from ai.decision.decision_engine import DecisionEngine
from ai.events.event_router import EventRouter
from ai.adaptive.adaptive_response import AdaptiveResponse

decision = DecisionEngine.decide(
    risk_level="HIGH",
    trust_score=20
)

route = EventRouter.route(
    "TRANSFER"
)

response = AdaptiveResponse.respond(
    "HIGH"
)

print(decision)
print(route)
print(response)
