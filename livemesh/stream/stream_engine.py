class StreamEngine:

    def synchronize(self, nodes):

        streams = []

        for node in nodes:

            streams.append({

                "node": node,

                "stream": "LIVE_SYNC",

                "status": "ACTIVE"
            })

        return streams
