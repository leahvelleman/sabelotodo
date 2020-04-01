import pytest, json, sys
from dataclasses import asdict
from itertools import product

from sabelotodo.models import Item



def test_create_item(_db):
    """ Verify that database works"""
    name = 'TestItem'
    done = True
    i = Item(name=name, order=0, done=done)

    _db.session.add(i)
    _db.session.commit()

    item = Item.query.filter_by(name=name).first()
    assert i == item


def test_item_route_with_empty_db(test_client, _db):
    return_value = test_client.get('/item')
    assert json.loads(return_value.data) == []


def test_item_route_with_multiple_items(test_client, _db):
    """ The /item route retrieves all items added. """

    items = [Item(name="a", order=0, done=False),
             Item(name="b", order=2, done=True),
             Item(name="c", order=1, done=False)]

    _db.session.add_all(items)
    _db.session.commit()

    return_value = test_client.get('/item')
    assert json.loads(return_value.data) == [asdict(i) for i in Item.query.all()]


@pytest.mark.parametrize("idx", [0, 1, 2])
def test_get_itemid_route_with_valid_id(test_client, _db, idx):
    """ The /item/<id> route retrieves just the item with the specified ID. """

    items = [Item(name="a", order=0, done=False),
             Item(name="b", order=2, done=True),
             Item(name="c", order=1, done=False)]

    _db.session.add_all(items)
    _db.session.commit()

    selection = items[idx]
    return_value = test_client.get('/item/%s' % selection.id)
    assert json.loads(return_value.data) == asdict(selection)


@pytest.mark.parametrize("idx", [0, 1, 2])
def test_delete_itemid_route_with_valid_id(test_client, _db, idx):
    """ A DELETE request to /item/<id> deletes the item with the
    specified ID. """

    items = [Item(name="a", order=0, done=False),
             Item(name="b", order=2, done=True),
             Item(name="c", order=1, done=False)]

    _db.session.add_all(items)
    _db.session.commit()

    selection = items[idx]
    remainder = items[:idx] + items[idx+1:]
    return_value = test_client.delete('/item/%s' % selection.id)
    assert return_value.status_code == 200
    assert sorted(Item.query.all()) == sorted(remainder)


def test_post_item_route(test_client):
    """ A POST request to /item creates an item with properties specified by
    the JSON payload. """

    item_json = {'name': 'a',
                 'order': 1,
                 'done': False,
                 'description': 'Lorem ipsum dolor sit amet',
                 'start_date': '2020-01-01',
                 'end_date': '2020-04-01',
                 'due_date': '2020-08-01'}

    return_value = test_client.post('/item', json=item_json)
    assert return_value.status_code == 200
    assert json.loads(return_value.data) == asdict(Item.query.all())
    

@pytest.mark.parametrize(
        "itemid, method", 
        product([sys.maxsize, "0.5", "-1", "1&garbage", "", "spork"],
                ["GET", "DELETE"]))
def test_itemid_route_failures(test_client, _db, itemid, method):
    """ The /item/<id> route fails with a 404 for IDs that don't convert to
    integers or that don't correspond to an item in the database, and
    does so for any of the methods we support. """

    items = [Item(name="a", order=0, done=False),
             Item(name="b", order=2, done=True),
             Item(name="c", order=1, done=False)]

    _db.session.add_all(items)
    _db.session.commit()

    return_value = test_client.open(method=method, path='/item/%s' % itemid)
    assert return_value.status_code == 404
