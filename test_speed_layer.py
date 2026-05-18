from infrastructure.cache.cache_engine import (
    CacheEngine
)

from infrastructure.session.session_engine import (
    SessionEngine
)

from infrastructure.rate_limit.rate_limiter import (
    RateLimiter
)

CacheEngine.set(

    "btc_price",

    105000
)

print(

    CacheEngine.get(
        "btc_price"
    )
)

token = SessionEngine.create_session(
    "rock"
)

print(token)

print(

    SessionEngine.validate(
        token
    )
)

for i in range(7):

    allowed = RateLimiter.allow(
        "127.0.0.1"
    )

    print(
        f"Request {i+1}:",
        allowed
    )
