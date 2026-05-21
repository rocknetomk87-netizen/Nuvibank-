class BrainEngine:

    def analyze(self, metrics):

        decisions = []

        for metric in metrics:

            if metric["latency"] > 100:

                decisions.append({

                    "system": metric["system"],

                    "decision": "REDISTRIBUTE_LOAD",

                    "priority": "HIGH"
                })

            else:

                decisions.append({

                    "system": metric["system"],

                    "decision": "KEEP_RUNNING",

                    "priority": "NORMAL"
                })

        return decisions
