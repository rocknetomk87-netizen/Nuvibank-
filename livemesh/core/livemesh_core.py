from livemesh.socket.socket_engine import (
    SocketEngine
)

from livemesh.events.event_stream import (
    EventStream
)

from livemesh.stream.stream_engine import (
    StreamEngine
)

from livemesh.runtime.livemesh_runtime import (
    LiveMeshRuntime
)


class LiveMeshCore:

    def __init__(self):

        self.socket = SocketEngine()

        self.events = EventStream()

        self.stream = StreamEngine()

        self.runtime = LiveMeshRuntime()

    def execute(self, nodes):

        connections = self.socket.connect(
            nodes
        )

        events = self.events.broadcast(
            nodes,
            "TRANSACTION_CONFIRMED"
        )

        streams = self.stream.synchronize(
            nodes
        )

        runtime = self.runtime.status()

        return {

            "connections": connections,

            "events": events,

            "streams": streams,

            "runtime": runtime
        }
