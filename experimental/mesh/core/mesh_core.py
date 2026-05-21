from mesh.discovery.discovery_engine import (
    DiscoveryEngine
)

from mesh.routing.routing_engine import (
    RoutingEngine
)

from mesh.health.health_engine import (
    HealthEngine
)

class MeshCore:

    def __init__(self):

        self.discovery = (
            DiscoveryEngine()
        )

        self.routing = (
            RoutingEngine()
        )

        self.health = (
            HealthEngine()
        )

    def register_service(

        self,

        name,
        host
    ):

        self.discovery.register(
            name,
            host
        )

    def send(

        self,

        service,
        payload
    ):

        target = (
            self.discovery
            .discover(service)
        )

        health = (
            self.health
            .check(service)
        )

        if not health["healthy"]:

            return {

                "error": "SERVICE_DOWN"
            }

        routed = (
            self.routing
            .route(
                target,
                payload
            )
        )

        return routed
