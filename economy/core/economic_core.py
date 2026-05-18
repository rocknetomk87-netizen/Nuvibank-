from economy.revenue.revenue_engine import (
    RevenueEngine
)

from economy.costs.cost_engine import (
    CostEngine
)

from economy.profit.profit_engine import (
    ProfitEngine
)

class EconomicCore:

    def __init__(self):

        self.revenue = (
            RevenueEngine()
        )

        self.costs = (
            CostEngine()
        )

        self.profit = (
            ProfitEngine()
        )

    def process(self):

        revenue = (
            self.revenue
            .calculate(
                1000000,
                0.02
            )
        )

        costs = (
            self.costs
            .calculate(
                50,
                120
            )
        )

        profit = (
            self.profit
            .calculate(
                revenue,
                costs
            )
        )

        return {

            "revenue": revenue,

            "costs": costs,

            "profit": profit
        }
