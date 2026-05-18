from architecture.modules.module_engine import (
    ModuleEngine
)

from architecture.dependencies.dependency_engine import (
    DependencyEngine
)

from architecture.flows.flow_engine import (
    FlowEngine
)

class ArchitectureCore:

    def __init__(self):

        self.modules = ModuleEngine()

        self.dependencies = DependencyEngine()

        self.flows = FlowEngine()

    def map(self):

        return {

            "modules": (
                self.modules.modules()
            ),

            "dependencies": (
                self.dependencies.dependencies()
            ),

            "flows": (
                self.flows.flows()
            )
        }
