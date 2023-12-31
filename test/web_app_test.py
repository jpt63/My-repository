# this is the "test/web_app_test.py" file...

# testing a flask app. see:
# ... https://github.com/prof-rossetti/intro-to-python/blob/main/notes/python/packages/flask.md#testing
# ... https://flask.palletsprojects.com/en/2.1.x/testing/

import pytest
from bs4 import BeautifulSoup

from web_app import create_app


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()


def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome Home" in response.data


def test_about(test_client):
    response = test_client.get("/about")
    assert response.status_code == 200
    assert b"About Me" in response.data


def test_hello(test_client):
    response = test_client.get("/hello")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

    # ... with url params
    response = test_client.get("/hello?name=MJR")
    assert response.status_code == 200
    assert b"Hello, MJR!" in response.data


def test_unemployment_dash(test_client):
    response = test_client.get("/unemployment/dashboard")
    assert response.status_code == 200
    assert b"Unemployment Dashboard" in response.data
    assert b"Latest Rate: " in response.data
    # using beautifulsoup to parse the response
    soup = BeautifulSoup(response.data, features="html.parser")
    rows = soup.find("tbody").find_all("tr")
    assert len(rows) == 12



def test_stocks_dash(test_client):
    #
    # DEFAULT SYMBOL
    #
    response = test_client.get("/stocks/dashboard")
    assert response.status_code == 200
    assert b"Stocks Dashboard (NFLX)" in response.data
    assert b"Latest Close: " in response.data

    #
    # CUSTOMIZED SYMBOL VIA URL PARAMS
    #
    response = test_client.get("/stocks/dashboard?symbol=GOOGL")
    assert response.status_code == 200
    assert b"Stocks Dashboard (GOOGL)" in response.data
    assert b"Latest Close: " in response.data