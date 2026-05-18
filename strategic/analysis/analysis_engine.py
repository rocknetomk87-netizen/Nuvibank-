class AnalysisEngine:

    def analyze_load(

        self,

        requests
    ):

        if requests > 1000:

            return "OVERLOAD"

        return "STABLE"
