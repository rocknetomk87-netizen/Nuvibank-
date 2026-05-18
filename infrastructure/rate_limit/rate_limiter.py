import time

class RateLimiter:

    requests = {}

    @classmethod
    def allow(
        cls,
        ip,
        limit=5,
        window=60
    ):

        now = time.time()

        if ip not in cls.requests:

            cls.requests[ip] = []

        cls.requests[ip] = [

            t for t in cls.requests[ip]

            if now - t < window
        ]

        if len(cls.requests[ip]) >= limit:

            return False

        cls.requests[ip].append(now)

        return True
