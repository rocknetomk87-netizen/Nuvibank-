class ContextEngine:

    def __init__(self):

        self.context = {}

    def update(
        self,
        key,
        value
    ):

        self.context[key] = value

    def state(self):

        return self.context
