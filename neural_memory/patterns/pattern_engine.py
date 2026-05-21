class PatternEngine:

    def detect(self, decisions):

        patterns = []

        for item in decisions:

            if item["decision"] == "REDISTRIBUTE_LOAD":

                patterns.append({

                    "system": item["system"],

                    "pattern": "HIGH_LOAD_PATTERN"
                })

            else:

                patterns.append({

                    "system": item["system"],

                    "pattern": "NORMAL_OPERATION"
                })

        return patterns
