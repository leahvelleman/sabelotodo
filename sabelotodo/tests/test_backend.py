import json


def test_empty_db(test_client, _db):
    rv = test_client.get('/item')
    assert json.loads(rv.data) == []
