class AnalysisEngine:

    def analyze(self, patterns):

        insights = []

        for item in patterns:

            if item["pattern"] == "HIGH_LOAD_PATTERN":

                insights.append({

                    "system": item["system"],

                    "prediction": "SCALING_REQUIRED"
                })

            else:

                insights.append({

                    "system": item["system"],

                    "prediction": "STABLE"
                })

        return insights
