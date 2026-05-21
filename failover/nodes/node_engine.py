class NodeEngine:

    def validate(self, nodes):

        active = []

        failed = []

        for node in nodes:

            if node["status"] == "ONLINE":

                active.append(node)

            else:

                failed.append(node)

        return {

            "active": active,

            "failed": failed
        }
