from fastapi.testclient import TestClient

from main import app
from tests.data import sample_data
from utils import alphavantage

client = TestClient(app)


def test_get_stocks_unauthorized():
    response = client.get("/stock-info/", params={"symbol": "IBM"})
    assert response.status_code == 401


def test_get_stocks_authorized():
    response = client.post("/token", data={"username": "test_username", "password": "password"})
    token = "Bearer " + response.json()["access_token"]

    response = client.get("/stock-info/", params={"symbol": "IBM"}, headers={"Authorization": token})
    assert response.status_code == 200


def test_alphavantage_mapping():
    expected_response = {
        "open_price": "140.6800",
        "higher_price": "140.6800",
        "lower_price": "138.6100",
        "variation_last_two_closing_price": 0.86
    }

    assert alphavantage.map_prices(sample_data.daily_stock_IBM_sample) == expected_response
