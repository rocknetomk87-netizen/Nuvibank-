class RoutingEngine:

    def route(

        self,

        service,
        payload
    ):

        return {

            "service": service,

            "payload": payload,

            "status": "ROUTED"
        }
