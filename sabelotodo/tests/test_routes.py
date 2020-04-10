import pytest
import sys
from itertools import product

from sabelotodo.models import Item, ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

VALID_ITEM_DATA = [{'name': 'minimal', 'order': 0, 'done': False},
                   {'name': 'has_start_date', 'order': 1, 'done': False,
                       'start_date': 'Sun, 06 Nov 94 08:49:37 -0000'},
                   {'name': 'has_description', 'order': 4, 'done': False,
                       'description': 'Lorem ipsum dolor sit amet.'},
                   {'name': 'already_done', 'order': 8, 'done': True}]

ADDITIONAL_VALID_ITEM_DATA = [{'name': 'a',
                               'order': 57,
                               'done': True},
                              {'name': 'a',
                               'order': 1,
                               'done': False,
                               'description': 'Lorem ipsum dolor sit amet',
                               'start_date': 'Sun, 05 Apr 20 19:22:13 -0000',
                               'due_date': 'Mon, 09 Nov 81 19:22:13 -0000',
                               'end_date': 'Sun, 08 Jun 56 19:22:13 -0000'}]

INVALID_ITEM_DATA = [{'name': 'name too long '*100,
                      'order': 57,
                      'done': True},
                     {'name': 'no order number',
                      'done': False},
                     {'name': 'unstandardized date format',
                      'order': 12,
                      'done': False,
                      'start_date': 'January 21, 2012'},
                     {'name': 'extraneous fields',
                      'order': 12,
                      'done': False,
                      'spatula': 'albuquerque'},
                     {}  # Empty JSON
                     ]

VALID_OVERWRITE_DATA = [{'name': 'name change only'},
                        {'name': 'name and doneness', 'done': True},
                        {'name': 'update that could overwrite a field',
                         'description': None},
                        {'name': 'name and date',
                         'start_date': 'Tue, 08 Nov 94 08:49:37 -0000'},
                        {'order': 12}]

INVALID_OVERWRITE_DATA = [{'name': None},  # Remove a required field
                          {'name': 'name too long '*100},
                          {'id': None},
                          {'start_date': 'January 21, 2012'},
                          {'id': 37},  # Primary key should be immutable,
                                       # since we use it as a foreign key
                          {},
                          {'done': 'asdf'}]  # Wrong type: string in a boolean field


@pytest.mark.parametrize("data", VALID_ITEM_DATA)
def test_create_item_from_empty(_db, data):
    """ An item can be added directly to an empty database. """
    item = item_schema.load(data)

    before = Item.query.all()
    _db.session.add(item)
    _db.session.commit()
    after = Item.query.all()

    created = [i for i in after if i not in before]
    assert created == [item], "Only the specified item is created."


@pytest.mark.parametrize("data", ADDITIONAL_VALID_ITEM_DATA)
def test_create_item_from_populated(_db, data):
    """ An item can be added directly to a populated database. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    item = item_schema.load(data)

    before = Item.query.all()
    _db.session.add(item)
    _db.session.commit()
    after = Item.query.all()

    created = [i for i in after if i not in before]

    assert created == [item], "Only the specified item is created."


def test_item_route_with_multiple_items(test_client, _db):
    """ The /item route retrieves all items added. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    return_value = test_client.get('/item')
    returned_items = items_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert returned_items == Item.query.all(), "Returned items match database."


@pytest.mark.parametrize("idx", range(len(VALID_ITEM_DATA)))
def test_get_itemid_route_with_valid_id(test_client, _db, idx):
    """ The /item/<id> route retrieves just the item with the specified ID. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    selection = items[idx]
    return_value = test_client.get('/item/%s' % selection.id)
    returned_item = item_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert returned_item == selection, "We get back the item we expect."


@pytest.mark.parametrize("idx", range(len(VALID_ITEM_DATA)))
def test_delete_itemid_route_with_valid_id(test_client, _db, idx):
    """ A DELETE request to /item/<id> deletes the item with the
    specified ID. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    selection = items[idx]
    remainder = items[:idx] + items[idx+1:]
    return_value = test_client.delete('/item/%s' % selection.id)
    returned_item = item_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert returned_item == selection, "We get back the item we expect."
    assert Item.query.all() == remainder, \
        "The remaining items are the ones we expect."

    get_attempt = test_client.get('/item/%s' % selection.id)
    assert get_attempt.status_code == 404, \
        "Attempting to get the item we deleted by ID fails."


@pytest.mark.parametrize("idx, overwrite_dict",
                         product(range(len(VALID_ITEM_DATA)),
                                 VALID_OVERWRITE_DATA))
def test_patch_itemid_route_with_valid_id(test_client, _db, idx, overwrite_dict):
    """ A PATCH request to /item/<id> overwrites the specified
    fields of the item with the specified ID. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    selection = items[idx]
    return_value = test_client.patch('/item/%s' % selection.id, json=overwrite_dict)

    assert return_value.status_code == 200, "The request succeeds."

    expected_dict = {**item_schema.dump(selection), **overwrite_dict}
    expected_item = item_schema.load(expected_dict)
    assert selection == expected_item, \
        "The selected item changes in the expected way."


@pytest.mark.parametrize("idx, overwrite_dict",
                         product(range(len(VALID_ITEM_DATA)), INVALID_OVERWRITE_DATA))
def test_patch_itemid_route_with_invalid_combinations(test_client, _db, idx, overwrite_dict):
    """ A PATCH request to /item/<id> overwrites the specified
    fields of the item with the specified ID. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    before = Item.query.all()
    selection = items[idx]
    return_value = test_client.patch('/item/%s' % selection.id, json=overwrite_dict)
    after = Item.query.all()

    assert return_value.status_code == 400, "The request fails."
    assert before == after, "Nothing changes."


@pytest.mark.parametrize("request_dict", ADDITIONAL_VALID_ITEM_DATA)
def test_post_item_route_with_valid_input(test_client, _db, request_dict):
    """ A POST request to /item creates an item with properties specified by
    the JSON payload. We specify _db as a fixture even though we don't use
    it so that the database will be torn down after each run. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    before = Item.query.all()
    return_value = test_client.post('/item', json=request_dict)
    returned_item = item_schema.loads(return_value.data)
    after = Item.query.all()
    created = [i for i in after if i not in before]

    assert return_value.status_code == 200, "The request succeeds."
    assert len(created) == 1, "One thing is created."
    assert returned_item == created[0], \
        "The return value matches what is created."


@pytest.mark.parametrize(
    "itemid, method",
    product([sys.maxsize, "0.5", "-1", "1&garbage", "", "spork"],
            ["GET", "DELETE", "PATCH"]))
def test_invalid_itemid(test_client, _db, itemid, method):
    """ The /item/<id> route fails with a 404 for IDs that don't convert to
    integers or that don't correspond to an item in the database, and
    does so for any of the methods we support. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    before = Item.query.all()
    return_value = test_client.open(method=method, path='/item/%s' % itemid)
    after = Item.query.all()

    assert return_value.status_code == 404, "The request fails."
    assert before == after, "Nothing changes."


@pytest.mark.parametrize("source_dict", INVALID_ITEM_DATA)
def test_invalid_post(test_client, _db, source_dict):
    """ The /item POST route fails with a 400 if you give it JSON that fails in
    various ways to satisfy the ItemSchema schema in models.py. """

    items = items_schema.load(VALID_ITEM_DATA)
    _db.session.add_all(items)
    _db.session.commit()

    before = Item.query.all()
    return_value = test_client.post('/item', json=source_dict)
    after = Item.query.all()

    assert return_value.status_code == 400, "The request fails."
    assert before == after, "Nothing changes."
