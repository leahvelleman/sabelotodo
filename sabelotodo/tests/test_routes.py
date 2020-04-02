import pytest, sys, datetime
from flask import json
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


@pytest.mark.parametrize("source_dict", 
        [{'name': 'a',
             'order': 57,
             'done': True},
         {'name': 'a', 
             'order': 1, 
             'done': False,
             'description': 'Lorem ipsum dolor sit amet',
             'start_date': datetime.datetime(2020,1,1,0,0)}
         ])
def test_post_item_route_with_valid_input(test_client, _db, source_dict):
    """ A POST request to /item creates an item with properties specified by
    the JSON payload. We specify _db as a fixture even though we don't use
    it so that the database will be torn down after each run. """

    return_value = test_client.post('/item', json=source_dict)
    returned_data = return_value.data
    created_item = Item.query.first()

    # The request succeeds.
    assert return_value.status_code == 200

    # The returned dictionary matches the created item in the database
    # modulo the effects of json encoding.
    assert json.loads(returned_data) == json.loads(json.dumps(created_item))

    # The created item we see in the database has attributes that are a
    # superset of the originally specified ones (they should go beyond it, for
    # instance, in containing an ID, and in containing default values for other
    # things that weren't specified).
    assert asdict(created_item).items() >= source_dict.items()
    
@pytest.mark.parametrize(
        "itemid, method", 
        product([sys.maxsize, "0.5", "-1", "1&garbage", "", "spork"],
                ["GET", "DELETE"]))
def test_invalid_itemid(test_client, _db, itemid, method):
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

#@pytest.mark.parametrize("source_dict", 
#        [{'name': 'name too long '*100,
#             'order': 57,
#             'done': True},
#         {'name': 'no order', 
#             'done': False}
#         ])
#def test_invalid_post(test_client, _db, source_dict):
#    return_value = test_client.post('/item', json=source_dict)
#
#    # The request fails with a 400 error.
#    assert return_value.status.code == 400
#
#    # Nothing is added to the database.
#    assert Item.query.all() == []
