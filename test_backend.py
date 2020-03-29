import os
import pytest
import json
from app import app, db
from models import Item

@pytest.fixture
def test_client():
    app.config['TESTING'] = True # For better error reporting
    with app.test_client() as client:
        yield client

def test_empty_db(test_client):
    rv = test_client.get('/item')
    assert json.loads(rv.data) == []

