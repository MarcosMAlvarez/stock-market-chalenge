from fastapi import status
from fastapi.responses import JSONResponse

from settings import MAX_LEN, SECONDS


class RateLimitException(Exception):
    pass


async def rate_limit_exception_handler(*args, **kwargs):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error msg": f"Rate-limit reached. The API call frequency is {MAX_LEN} per {SECONDS} seconds."
        },
    )


def include_app(app):
    app.add_exception_handler(RateLimitException, rate_limit_exception_handler)
