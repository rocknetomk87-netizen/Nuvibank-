class RevenueEngine:

    def calculate(

        self,

        transfers,
        fee
    ):

        revenue = (
            transfers * fee
        )

        return revenue
