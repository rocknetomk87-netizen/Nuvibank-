class RuleEngine:

    def validate(self, event):

        critical = [

            "FRAUD",
            "SYSTEM_ATTACK",
            "BREACH"
        ]

        if event in critical:

            return {

                "allowed": False,

                "reason": "CRITICAL_EVENT"
            }

        return {

            "allowed": True
        }
