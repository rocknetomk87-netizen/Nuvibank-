from live.events.event_engine import EventEngine
from live.analysis.analysis_engine import AnalysisEngine
from live.execution.execution_engine import ExecutionEngine
from live.state.state_engine import StateEngine


class LiveCore:

    def __init__(self):

        self.event_engine = EventEngine()
        self.analysis_engine = AnalysisEngine()
        self.execution_engine = ExecutionEngine()
        self.state_engine = StateEngine()

    def process(self):

        event = self.event_engine.next_event()

        analysis = self.analysis_engine.analyze(event)

        execution = self.execution_engine.execute(analysis)

        state = self.state_engine.update(event)

        return {
            "event": event,
            "analysis": analysis,
            "execution": execution,
            "state": state
        }
