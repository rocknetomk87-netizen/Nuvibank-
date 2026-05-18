from scaling.adaptive.adaptive_scaler import (
    AdaptiveScaler
)

class ScaleCore:

    @staticmethod
    def run(load):

        workers = AdaptiveScaler.analyze(
            load
        )

        print(
            "[ACTIVE WORKERS]",
            workers
        )
