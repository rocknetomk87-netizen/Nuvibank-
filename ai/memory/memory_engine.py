class MemoryEngine:

    memory = {}

    @classmethod
    def remember(
        cls,
        username,
        event
    ):

        if username not in cls.memory:

            cls.memory[username] = []

        cls.memory[username].append(event)

    @classmethod
    def get_memory(
        cls,
        username
    ):

        return cls.memory.get(
            username,
            []
        )
