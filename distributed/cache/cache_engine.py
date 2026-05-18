class CacheEngine:

    cache = {}

    @classmethod
    def set(

        cls,

        key,

        value
    ):

        cls.cache[key] = value

    @classmethod
    def get(

        cls,

        key
    ):

        return cls.cache.get(key)

    @classmethod
    def exists(

        cls,

        key
    ):

        return key in cls.cache

    @classmethod
    def delete(

        cls,

        key
    ):

        if key in cls.cache:

            del cls.cache[key]
