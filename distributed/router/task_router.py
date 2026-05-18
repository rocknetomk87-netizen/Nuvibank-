class TaskRouter:

    @staticmethod
    def route(

        nodes,

        task
    ):

        for node in nodes:

            if node.available():

                node.assign_task(task)

                return node.node_id

        return None
