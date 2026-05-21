from boot.loader.boot_loader import BootLoader
from boot.runtime.runtime_boot import RuntimeBoot


class BootCore:

    def __init__(self):

        self.loader = BootLoader()

        self.runtime = RuntimeBoot()

    def boot(self):

        loader = self.loader.load()

        runtime = self.runtime.initialize()

        return {
            "boot": "SYSTEM_INITIALIZED",
            "loader": loader,
            "runtime": runtime
        }
