import pytest
from itertools import product

from sabelotodo.models import Item, ItemSchema
from .helpers import populate
from .testdata import VALID_ITEM_DATA, ADDITIONAL_VALID_ITEM_DATA, \
        INVALID_ITEM_DATA, VALID_OVERWRITE_DATA, INVALID_OVERWRITE_DATA, \
        INVALID_ID_NUMBERS

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


def test_item_route_with_multiple_items(test_client, _db):
    """ The /item route retrieves all items added. """

    populate(_db, items_schema, VALID_ITEM_DATA)

    return_value = test_client.get('/item')
    return_dicts = items_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert len(return_dicts) == len(VALID_ITEM_DATA), "We get everything."


@pytest.mark.parametrize("idx", range(len(VALID_ITEM_DATA)))
def test_get_itemid_route_with_valid_id(test_client, _db, idx):
    """ The /item/<id> route retrieves just the item with the specified ID. """

    items = populate(_db, items_schema, VALID_ITEM_DATA)

    selection = items[idx]
    return_value = test_client.get('/item/%s' % selection.id)
    return_dict = item_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    return_dict = item_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert return_dict['id'] == selection.id, "The ID matches."
    assert return_dict['name'] == selection.name, "The name matches."
    assert return_dict['order'] == selection.order, "The order number matches."
    assert return_dict['done'] == selection.done, "The doneness matches."
    assert return_dict['description'] == selection.description, \
        "The description matches."
    assert return_dict['start_date'] == selection.start_date, \
        "The start date matches."
    assert return_dict['end_date'] == selection.end_date, \
        "The end date matches."
    assert return_dict['due_date'] == selection.due_date, \
        "The due date matches."
    assert return_dict['parent_id'] == selection.parent_id, \
        "The parent ID matches."


@pytest.mark.parametrize("idx", range(len(VALID_ITEM_DATA)))
def test_delete_itemid_route_with_valid_id(test_client, _db, idx):
    """ A DELETE request to /item/<id> deletes the item with the
    specified ID. """

    items = populate(_db, items_schema, VALID_ITEM_DATA)

    selection = items[idx]
    remainder = items[:idx] + items[idx+1:]
    return_value = test_client.delete('/item/%s' % selection.id)
    return_dict = item_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert return_dict['id'] == selection.id, "The ID matches."
    assert return_dict['name'] == selection.name, "The name matches."
    assert return_dict['order'] == selection.order, "The order number matches."
    assert return_dict['done'] == selection.done, "The doneness matches."
    assert return_dict['description'] == selection.description, \
        "The description matches."
    assert return_dict['start_date'] == selection.start_date, \
        "The start date matches."
    assert return_dict['end_date'] == selection.end_date, \
        "The end date matches."
    assert return_dict['due_date'] == selection.due_date, \
        "The due date matches."
    assert return_dict['parent_id'] == selection.parent_id, \
        "The parent ID matches."
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

    items = populate(_db, items_schema, VALID_ITEM_DATA)

    selection = items[idx]
    expected_dict = {**item_schema.dump(selection), **overwrite_dict}
    return_value = test_client.patch('/item/%s' % selection.id,
                                     json=overwrite_dict)
    return_dict = item_schema.dump(selection)

    assert return_value.status_code == 200, "The request succeeds."

    assert expected_dict == return_dict, \
        "The returned dict has the values we expect."


@pytest.mark.parametrize("idx, overwrite_dict",
                         product(range(len(VALID_ITEM_DATA)), INVALID_OVERWRITE_DATA))
def test_patch_itemid_route_with_invalid_combinations(test_client, _db, idx, overwrite_dict):
    """ A PATCH request to /item/<id> overwrites the specified
    fields of the item with the specified ID. """

    items = populate(_db, items_schema, VALID_ITEM_DATA)

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

    populate(_db, items_schema, VALID_ITEM_DATA)

    before = Item.query.all()
    return_value = test_client.post('/item', json=request_dict)
    return_dict = item_schema.loads(return_value.data)
    after = Item.query.all()

    created = [i for i in after if i not in before]

    assert return_value.status_code == 200, "The request succeeds."
    assert len(created) == 1, "One thing is created."
    assert return_dict['id'] == created[0].id, "The ID matches."
    assert return_dict['name'] == created[0].name, "The name matches."
    assert return_dict['order'] == created[0].order, "The order number matches."
    assert return_dict['done'] == created[0].done, "The doneness matches."
    assert return_dict['description'] == created[0].description, \
        "The description matches."
    assert return_dict['start_date'] == created[0].start_date, \
        "The start date matches."
    assert return_dict['end_date'] == created[0].end_date, \
        "The end date matches."
    assert return_dict['due_date'] == created[0].due_date, \
        "The due date matches."
    assert return_dict['parent_id'] == created[0].parent_id, \
        "The parent ID matches."


@pytest.mark.parametrize(
    "itemid, method", product(INVALID_ID_NUMBERS, ["GET", "DELETE", "PATCH"]))
def test_invalid_itemid(test_client, _db, itemid, method):
    """ The /item/<id> route fails with a 404 for IDs that don't convert to
    integers or that don't correspond to an item in the database, and
    does so for any of the methods we support. """

    populate(_db, items_schema, VALID_ITEM_DATA)

    before = Item.query.all()
    return_value = test_client.open(method=method, path='/item/%s' % itemid)
    after = Item.query.all()

    assert return_value.status_code == 404, "The request fails."
    assert before == after, "Nothing changes."


@pytest.mark.parametrize("source_dict", INVALID_ITEM_DATA)
def test_invalid_post(test_client, _db, source_dict):
    """ The /item POST route fails with a 400 if you give it JSON that fails in
    various ways to satisfy the ItemSchema schema in models.py. """

    populate(_db, items_schema, VALID_ITEM_DATA)

    before = Item.query.all()
    return_value = test_client.post('/item', json=source_dict)
    after = Item.query.all()

    assert return_value.status_code == 400, "The request fails."
    assert before == after, "Nothing changes."
