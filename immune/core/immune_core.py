from immune.firewall.firewall_engine import FirewallEngine
from immune.quarantine.quarantine_engine import QuarantineEngine
from immune.adaptive.adaptive_engine import AdaptiveEngine


class ImmuneCore:

    def __init__(self):

        self.firewall = FirewallEngine()
        self.quarantine = QuarantineEngine()
        self.adaptive = AdaptiveEngine()

    def defend(self, threats):

        firewall = self.firewall.inspect(threats)

        quarantine = self.quarantine.isolate(firewall)

        adaptive = self.adaptive.adapt(quarantine)

        return {
            "threats": threats,
            "firewall": firewall,
            "quarantine": quarantine,
            "adaptive": adaptive,
            "status": "IMMUNE_SYSTEM_ACTIVE"
        }
