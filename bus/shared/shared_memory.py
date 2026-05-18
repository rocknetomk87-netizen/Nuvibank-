class SharedMemory:

    def __init__(self):

        self.memory = {}

    def store(
        self,
        module,
        data
    ):

        self.memory[module] = data

    def read_all(self):

        return self.memory
