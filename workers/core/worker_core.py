from workers.queue.queue_engine import QueueEngine
from workers.dispatch.dispatch_engine import DispatchEngine
from workers.execution.execution_engine import ExecutionEngine
from workers.balancing.balancer_engine import BalancerEngine


class WorkerCore:

    def __init__(self):

        self.queue_engine = QueueEngine()
        self.dispatch_engine = DispatchEngine()
        self.execution_engine = ExecutionEngine()
        self.balancer_engine = BalancerEngine()

    def run(self):

        tasks = self.queue_engine.tasks()

        dispatched = self.dispatch_engine.dispatch(tasks)

        executed = self.execution_engine.execute(dispatched)

        balance = self.balancer_engine.balance()

        return {
            "tasks": tasks,
            "dispatched": dispatched,
            "executed": executed,
            "balance": balance
        }
