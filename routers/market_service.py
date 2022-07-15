from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status

from utils import alphavantage, authentication, throttling
from settings import MAX_LEN, SECONDS, oauth2_scheme


router = APIRouter()





@router.get("/stock-info/", tags=["market_service"])
@throttling.rate_limit(maxlen=MAX_LEN, seconds=SECONDS)
async def get_stock_information(symbol: str, token: str = Depends(oauth2_scheme)):
    """Call Alpha Vantage API to retrieve stock information from the stock symbol
    passed as a header request.

    It's necessary to be an authorized user to consume the endpoint. The service return
    a json with the open, high and low price values, and the variation between the
    last two closing price values."""
    await authentication.check_credentials(token)

    # Pass datetime info to call_alphavantage to update cache
    now = datetime.now()
    date_time = (now.year, now.month, now.day, "AM" if now.hour < 12 else "PM")
    response = alphavantage.call_alphavantage(symbol, date_time=date_time)

    try:
        daily_stock_info = response.json()["Time Series (Daily)"]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Oops, something went wrong, try again.",
        )
    else:
        return {symbol: alphavantage.map_prices(daily_stock_info)}
