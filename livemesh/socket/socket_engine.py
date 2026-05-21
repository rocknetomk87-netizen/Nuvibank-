class SocketEngine:

    def connect(self, nodes):

        connections = []

        for node in nodes:

            connections.append({

                "node": node,

                "socket": "CONNECTED",

                "status": "ONLINE"
            })

        return connections
