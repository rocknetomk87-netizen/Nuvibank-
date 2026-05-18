class SchedulerEngine:

    def schedule(
        self,
        task
    ):

        return {

            "task": task,

            "scheduled": True,

            "queue": "PRIMARY"
        }
