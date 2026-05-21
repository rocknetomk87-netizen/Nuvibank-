from logger.system.system_logger import SystemLogger
from logger.security.security_logger import SecurityLogger
from logger.runtime.runtime_logger import RuntimeLogger
from logger.events.event_logger import EventLogger

class LoggerCore:

    def __init__(self):

        self.system = SystemLogger()

        self.security = SecurityLogger()

        self.runtime = RuntimeLogger()

        self.events = EventLogger()

    def full_log(self):

        return {

            "system":
                self.system.log(
                    "INFO",
                    "NUVIBANK ONLINE"
                ),

            "security":
                self.security.alert(
                    "FRAUD_ALERT",
                    "HIGH"
                ),

            "runtime":
                self.runtime.runtime(
                    1,
                    "RUNNING"
                ),

            "event":
                self.events.event(
                    "LOCKDOWN"
                )
        }
