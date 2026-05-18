class SystemMonitor:

    state = {

        "cpu": 30,

        "memory": 40,

        "requests": 120,

        "fraud_alerts": 2,

        "active_nodes": 3
    }

    @classmethod
    def get_state(cls):

        return cls.state
