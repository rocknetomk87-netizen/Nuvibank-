from livemesh.core.livemesh_core import (
    LiveMeshCore
)

mesh = LiveMeshCore()

nodes = [

    "node-1",

    "node-2",

    "node-3"
]

result = mesh.execute(
    nodes
)

print(result)
