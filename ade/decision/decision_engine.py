class DecisionEngine:

    def execute(self, decisions):

        executed = []

        for item in decisions:

            executed.append({

                "system": item["system"],

                "decision": item["decision"],

                "execution": "COMPLETED"
            })

        return executed
