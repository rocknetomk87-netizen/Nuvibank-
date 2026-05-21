from sentinel.watchers.watcher_engine import (
    WatcherEngine
)

from sentinel.anomaly.anomaly_engine import (
    AnomalyEngine
)

from sentinel.monitor.monitor_engine import (
    MonitorEngine
)

class SentinelCore:

    def __init__(self):

        self.watcher = WatcherEngine()

        self.anomaly = AnomalyEngine()

        self.monitor = MonitorEngine()

    def scan(self):

        events = (
            self.watcher.watch()
        )

        anomalies = (
            self.anomaly.detect(
                events
            )
        )

        status = (
            self.monitor.classify(
                anomalies
            )
        )

        return {

            "events": events,

            "anomalies": anomalies,

            "status": status
        }
