class LearningEngine:

    def learn(self, decisions):

        learned = []

        for item in decisions:

            learned.append({

                "system": item["system"],

                "pattern": item["decision"],

                "memory": "STORED"
            })

        return learned
