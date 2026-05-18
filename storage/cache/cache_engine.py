class CacheEngine:

    def cache(self, payload):

        return {
            "cached": True,
            "payload": payload,
            "memory": "FAST_ACCESS"
        }
