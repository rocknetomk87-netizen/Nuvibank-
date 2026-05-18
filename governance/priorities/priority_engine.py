class PriorityEngine:

    def get_priority(self, event):

        priorities = {

            "FRAUD": 10,
            "BREACH": 10,
            "SYSTEM_ATTACK": 10,

            "TRANSFER": 7,
            "LOGIN": 5,

            "NOTIFICATION": 2
        }

        return priorities.get(
            event,
            1
        )
