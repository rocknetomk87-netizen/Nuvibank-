class MemoryStore:

    def __init__(self):

        self.memory = []

    def save(self, pattern):

        self.memory.append(pattern)

        return {

            "saved": pattern,

            "status": "STORED"
        }

    def all(self):

        return self.memory
