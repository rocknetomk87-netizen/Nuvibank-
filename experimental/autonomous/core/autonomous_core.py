from autonomous.actions.action_engine import (
    ActionEngine
)

from autonomous.workflows.workflow_engine import (
    WorkflowEngine
)

from autonomous.execution.execution_engine import (
    ExecutionEngine
)

class AutonomousCore:

    def __init__(self):

        self.actions = (
            ActionEngine()
        )

        self.workflows = (
            WorkflowEngine()
        )

        self.execution = (
            ExecutionEngine()
        )

    def react(

        self,

        event
    ):

        workflow = (
            self.workflows
            .run(event)
        )

        executed = (
            self.execution
            .dispatch(workflow)
        )

        return {

            "event": event,

            "workflow":
            workflow,

            "executed":
            executed
        }
