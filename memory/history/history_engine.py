class HistoryEngine:

    def __init__(self):

        self.history = []

    def store(

        self,

        event
    ):

        self.history.append(event)

    def get_all(self):

        return self.history
