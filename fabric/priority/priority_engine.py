class PriorityEngine:

    def priority(
        self,
        event
    ):

        priorities = {

            "FRAUD": 10,

            "TRANSFER": 7,

            "LOGIN": 3
        }

        return priorities.get(
            event,
            1
        )
