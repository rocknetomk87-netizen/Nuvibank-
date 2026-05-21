class VotingEngine:

    def vote(self, nodes):

        approvals = 0

        for node in nodes:

            if node["status"] == "ONLINE":

                approvals += 1

        return approvals >= (
            len(nodes) // 2 + 1
        )
