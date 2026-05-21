class EventStream:

    def broadcast(self, nodes, event):

        stream = []

        for node in nodes:

            stream.append({

                "node": node,

                "event": event,

                "broadcast": "DELIVERED"
            })

        return stream
