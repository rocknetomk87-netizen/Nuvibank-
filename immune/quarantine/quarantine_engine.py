class QuarantineEngine:

    def isolate(self, firewall):

        if firewall.get("firewall_action") == "BLOCK":
            return {
                "isolated": True,
                "quarantine": "ACTIVE",
                "status": "THREAT_CONTAINED"
            }

        return {
            "isolated": False,
            "quarantine": "STANDBY",
            "status": "SAFE"
        }
