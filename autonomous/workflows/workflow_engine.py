class WorkflowEngine:

    def run(

        self,

        event
    ):

        workflows = {

            "FRAUD": [

                "LOCK_ACCOUNT",

                "BLOCK_IP",

                "ENABLE_MFA",

                "ALERT_SECURITY"
            ],

            "TRANSFER": [

                "VERIFY_BALANCE",

                "PROCESS_PAYMENT"
            ]
        }

        return workflows.get(
            event,
            []
        )
