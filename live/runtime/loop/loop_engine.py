import time

from live.core.live_core import LiveCore


class LoopEngine:

    def __init__(self):

        self.live = LiveCore()

    def run(self, cycles=3):

        results = []

        for cycle in range(cycles):

            result = self.live.process()

            results.append({
                "cycle": cycle + 1,
                "result": result
            })

            time.sleep(1)

        return results
