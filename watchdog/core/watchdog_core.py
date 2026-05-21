from watchdog.checks.health_check import (
    HealthCheck
)

from watchdog.alerts.alert_engine import (
    AlertEngine
)

from watchdog.runtime.watchdog_runtime import (
    WatchdogRuntime
)


class WatchdogCore:

    def __init__(self):

        self.check = HealthCheck()

        self.alert = AlertEngine()

        self.runtime = WatchdogRuntime()

    def monitor(self, systems):

        report = self.check.inspect(
            systems
        )

        alerts = self.alert.process(
            report
        )

        runtime = self.runtime.status()

        return {

            "report": report,

            "alerts": alerts,

            "runtime": runtime
        }
