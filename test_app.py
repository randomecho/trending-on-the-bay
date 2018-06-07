import os
import pytest
import app

@pytest.fixture
def client():
    client = app.app.test_client()
    yield client

def test_homepage(client):
    rv = client.get("/")
    assert b"Trending on the Bay" in rv.data

def test_missing(client):
    rv = client.get("/page-that-does-not-exist")
    assert b"Missing" in rv.data
    assert rv.status_code == 404
