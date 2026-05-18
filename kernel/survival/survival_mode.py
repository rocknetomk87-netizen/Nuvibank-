class SurvivalMode:

    def activate(

        self,

        threat_level
    ):

        if threat_level >= 8:

            return {

                "mode": "LOCKDOWN",

                "mfa": True,

                "transfer_limit": True,

                "ip_block": True
            }

        return {

            "mode": "NORMAL"
        }
