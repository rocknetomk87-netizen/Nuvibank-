class PriorityEngine:

    PRIORITY_MAP = {
        "HIGH": 1,
        "NORMAL": 2,
        "LOW": 3
    }

    def sort_tasks(self, tasks):

        return sorted(
            tasks,
            key=lambda task:
            self.PRIORITY_MAP.get(
                task["priority"],
                99
            )
        )
