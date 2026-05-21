from neural_memory.storage.memory_store import (
    MemoryStore
)

from neural_memory.patterns.pattern_engine import (
    PatternEngine
)

from neural_memory.analysis.analysis_engine import (
    AnalysisEngine
)

from neural_memory.runtime.neural_runtime import (
    NeuralRuntime
)


class NeuralCore:

    def __init__(self):

        self.store = MemoryStore()

        self.patterns = PatternEngine()

        self.analysis = AnalysisEngine()

        self.runtime = NeuralRuntime()

    def process(self, decisions):

        patterns = self.patterns.detect(
            decisions
        )

        stored = []

        for pattern in patterns:

            stored.append(
                self.store.save(pattern)
            )

        insights = self.analysis.analyze(
            patterns
        )

        runtime = self.runtime.status()

        return {

            "patterns": patterns,

            "stored": stored,

            "insights": insights,

            "memory": self.store.all(),

            "runtime": runtime
        }
