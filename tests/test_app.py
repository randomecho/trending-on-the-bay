import pytest
from app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_homepage(client):
    rv = client.get("/")
    assert b"Trending on the Bay" in rv.data


def test_missing(client):
    rv = client.get("/page-that-does-not-exist")
    assert b"Missing" in rv.data
    assert rv.status_code == 404


def test_search(client):
    rv = client.get("/search?keyword=chog")
    assert b"results for: <b>chog</b>" in rv.data

    with app.test_request_context("/search?keyword=chog") as req:
        assert req.request.args['keyword'] == 'chog'
