class StateEngine:

    def __init__(self):

        self.global_state = {}

    def update(

        self,

        key,
        value
    ):

        self.global_state[key] = value

    def get_state(self):

        return self.global_state
