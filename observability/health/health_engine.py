class HealthEngine:

    @staticmethod
    def node_status(

        node_name,

        cpu,

        memory
    ):

        if cpu > 90:

            return {

                "node": node_name,

                "status": "CRITICAL"
            }

        if memory > 90:

            return {

                "node": node_name,

                "status": "HIGH_MEMORY"
            }

        return {

            "node": node_name,

            "status": "HEALTHY"
        }
