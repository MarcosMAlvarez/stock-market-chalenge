from collections import deque
from datetime import datetime
from functools import wraps

from settings import MAX_LEN
from utils.exceptions import RateLimitException

deq = deque(maxlen=MAX_LEN)  # type: deque


def rate_limit(maxlen, seconds):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global deq
            current_time = datetime.now()
            if len(deq) != 0:
                if len(deq) == maxlen and (current_time - deq[0]).seconds < seconds:
                    raise RateLimitException()
            deq.append(current_time)
            return await func(*args, **kwargs)

        return wrapper

    return inner
