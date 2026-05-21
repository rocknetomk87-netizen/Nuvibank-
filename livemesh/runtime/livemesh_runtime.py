from datetime import datetime


class LiveMeshRuntime:

    def status(self):

        return {

            "runtime": "LIVE_MESH_ACTIVE",

            "timestamp": str(datetime.utcnow()),

            "status": "RUNNING"
        }
