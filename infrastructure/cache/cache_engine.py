import time

class CacheEngine:

    cache = {}

    @classmethod
    def set(
        cls,
        key,
        value,
        ttl=60
    ):

        cls.cache[key] = {

            "value": value,

            "expires": time.time() + ttl
        }

    @classmethod
    def get(
        cls,
        key
    ):

        data = cls.cache.get(key)

        if not data:

            return None

        if time.time() > data["expires"]:

            del cls.cache[key]

            return None

        return data["value"]
