"""Stock Market Challenge API
"""
from fastapi import FastAPI

from routers import market_service, users
from utils import exceptions


app = FastAPI(title="Stock Market Challenge", version="0.0.1")
app.include_router(users.router)
app.include_router(market_service.router)

exceptions.include_app(app)


@app.get("/")
async def root():
    return {"msg": "stock market challenge"}


if __name__ == "__main__":
    import os

    from uvicorn import Config, Server

    import logs.utils

    ON_HEROKU = os.environ.get("ON_HEROKU")

    if ON_HEROKU:
        # get the heroku port
        port = int(os.environ.get("PORT", 17995))
    else:
        port = 8000

    server = Server(
        Config("main:app", host="0.0.0.0", port=port, log_level=logs.utils.LOG_LEVEL),
    )

    # setup logging last, to make sure no library overwrites it
    logs.utils.setup_logging()
    server.run()
