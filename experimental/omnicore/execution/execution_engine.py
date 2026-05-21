class ExecutionEngine:

    def execute(self, decision):

        return {
            "decision": decision,
            "executed": True,
            "status": "EXECUTION_COMPLETE"
        }
