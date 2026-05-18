class NodeEngine:

    def __init__(

        self,

        node_id,

        capacity
    ):

        self.node_id = node_id

        self.capacity = capacity

        self.active_tasks = 0

    def available(self):

        return self.active_tasks < self.capacity

    def assign_task(

        self,

        task
    ):

        self.active_tasks += 1

        print(

            f"[NODE {self.node_id}]",

            task
        )

    def complete_task(self):

        if self.active_tasks > 0:

            self.active_tasks -= 1
