from slowapi import Limiter
from slowapi.util import get_remote_address

def init_rate_limiter(rate_limit):
    """
    Initialize the rate limiter with the default rate limit.

    Args:
        rate_limit (str): Rate limit string (e.g., "100/hour").

    Returns (Limiter): Configured Limiter instance.
    """
    return Limiter(key_func=get_remote_address, default_limits=[rate_limit])
