from functools import lru_cache

import requests

from settings import AV_APIKEY


# pylint: disable=unused-argument
@lru_cache
def call_alphavantage(symbol: str, **kwargs):
    """Call the alpha vantage api with cache to avoid exhausting the allowed api calls.
    Date_time argument is used to update the information retrieved from alpha vantage
    up to twice a day"""
    url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}"
        + f"&outputsize=compact&apikey={AV_APIKEY}"
    )

    return requests.get(url)


def map_prices(daily_stock_info: dict) -> dict:
    """Return only the needed data."""
    current_day, last_day, *_ = sorted(daily_stock_info, reverse=True)

    needed_info = {
        "open_price": daily_stock_info[current_day]["1. open"],
        "higher_price": daily_stock_info[current_day]["2. high"],
        "lower_price": daily_stock_info[current_day]["3. low"],
        "variation_last_two_closing_price": round(
            float(daily_stock_info[current_day]["4. close"]) - float(daily_stock_info[last_day]["4. close"]),
            4,
        ),
    }

    return needed_info
