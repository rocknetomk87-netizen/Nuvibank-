class PriorityEngine:

    def get_priority(

        self,

        event_type
    ):

        priorities = {

            "FRAUD": 10,

            "SECURITY": 9,

            "TRANSFER": 7,

            "AI_ANALYSIS": 6,

            "NOTIFICATION": 3
        }

        return priorities.get(
            event_type,
            1
        )
