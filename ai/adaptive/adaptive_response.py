class AdaptiveResponse:

    @staticmethod
    def respond(risk_level):

        if risk_level == "HIGH":

            return {
                "mfa_required": True,
                "transfer_locked": True
            }

        if risk_level == "MEDIUM":

            return {
                "mfa_required": True,
                "transfer_locked": False
            }

        return {
            "mfa_required": False,
            "transfer_locked": False
        }
