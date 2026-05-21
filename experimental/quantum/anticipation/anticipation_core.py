from quantum.predict.predict_engine import (
    PredictEngine
)

from quantum.preload.preload_engine import (
    PreloadEngine
)

class AnticipationCore:

    def __init__(self):

        self.predict = PredictEngine()

        self.preload = PreloadEngine()

    def execute(

        self,

        profile
    ):

        predictions = (
            self.predict
            .predict_next_actions(
                profile
            )
        )

        preloaded = (
            self.preload
            .preload_data(
                predictions
            )
        )

        return {

            "predictions":
            predictions,

            "preloaded":
            preloaded
        }
