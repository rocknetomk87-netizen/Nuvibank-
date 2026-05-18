from temporal.history.history_engine import (
    HistoryEngine
)

from temporal.patterns.pattern_engine import (
    PatternEngine
)

from temporal.predictions.predict_engine import (
    PredictEngine
)

class TemporalCore:

    def __init__(self):

        self.history = HistoryEngine()

        self.patterns = PatternEngine()

        self.predictor = PredictEngine()

    def analyze(self):

        events = (
            self.history.load_events()
        )

        patterns = (
            self.patterns.detect_patterns(
                events
            )
        )

        prediction = (
            self.predictor.predict(
                patterns
            )
        )

        return {

            "patterns": patterns,

            "prediction": prediction
        }
