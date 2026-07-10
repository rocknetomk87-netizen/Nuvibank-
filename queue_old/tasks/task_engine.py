class TaskEngine:

    def create_task(
        self,
        name,
        payload,
        priority="NORMAL"
    ):

        return {
            "task": name,
            "payload": payload,
            "priority": priority,
            "status": "QUEUED"
        }
