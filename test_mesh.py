from mesh.core.mesh_core import (
    MeshCore
)

mesh = MeshCore()

mesh.register_service(

    "PAYMENT",

    "NODE-1"
)

mesh.register_service(

    "SECURITY",

    "NODE-2"
)

result = mesh.send(

    "PAYMENT",

    {
        "amount": 5000
    }
)

print(result)
