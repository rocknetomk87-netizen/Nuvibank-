from datetime import datetime


class RuntimeBoot:

    def initialize(self):

        return {
            "runtime_boot": "ACTIVE",
            "boot_time": str(datetime.utcnow()),
            "status": "RUNNING"
        }
