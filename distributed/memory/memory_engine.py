class DistributedMemory:

    memory = {}

    @classmethod
    def store(

        cls,

        key,

        value
    ):

        cls.memory[key] = value

    @classmethod
    def retrieve(

        cls,

        key
    ):

        return cls.memory.get(key)
