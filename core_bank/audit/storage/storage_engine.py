class StorageEngine:

    def __init__(self):

        self.logs = []

    def store(

        self,

        log
    ):

        self.logs.append(log)

    def all_logs(self):

        return self.logs
