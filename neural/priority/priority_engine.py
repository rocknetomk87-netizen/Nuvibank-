class PriorityEngine:

    def calculate_priority(

        self,

        task
    ):

        if task["type"] == "FRAUD_CHECK":

            return 10

        if task["type"] == "TRANSFER":

            return 8

        if task["type"] == "LOGIN":

            return 5

        return 1
