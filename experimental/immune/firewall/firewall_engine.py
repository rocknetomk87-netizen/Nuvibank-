class FirewallEngine:

    def inspect(self, threats):

        attacks = threats.get("attacks", 0)

        if attacks >= 10:
            return {
                "firewall_action": "BLOCK",
                "status": "PROTECTION_ENABLED",
                "risk": "HIGH"
            }

        return {
            "firewall_action": "MONITOR",
            "status": "MONITORING",
            "risk": "LOW"
        }
