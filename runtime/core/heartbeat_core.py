from runtime.heartbeat.heartbeat_engine import HeartbeatEngine
from runtime.health.health_engine import HealthEngine
from runtime.vitals.vitals_engine import VitalsEngine


class HeartbeatCore:
    def __init__(self):
        self.heartbeat = HeartbeatEngine()
        self.health = HealthEngine()
        self.vitals = VitalsEngine()

    def run(self):
        return {
            "heartbeat": self.heartbeat.beat(),
            "health": self.health.check(),
            "vitals": self.vitals.status()
        }
