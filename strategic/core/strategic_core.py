from strategic.predict.predict_engine import (
    PredictEngine
)

from strategic.analysis.analysis_engine import (
    AnalysisEngine
)

from strategic.forecast.forecast_engine import (
    ForecastEngine
)

class StrategicCore:

    def __init__(self):

        self.predict = (
            PredictEngine()
        )

        self.analysis = (
            AnalysisEngine()
        )

        self.forecast = (
            ForecastEngine()
        )

    def think(self):

        risk = (
            self.predict
            .predict_risk(8)
        )

        load = (
            self.analysis
            .analyze_load(1500)
        )

        growth = (
            self.forecast
            .forecast_growth(100000)
        )

        return {

            "risk": risk,

            "load": load,

            "growth": growth
        }
