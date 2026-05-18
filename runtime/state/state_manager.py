class StateManager:
    def __init__(self):
        self.state = {
            "system": "NUVIBANK™",
            "status": "ONLINE"
        }

    def update(self, key, value):
        self.state[key] = value

    def get(self):
        return self.state
