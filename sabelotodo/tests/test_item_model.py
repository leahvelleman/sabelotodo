import pytest
from datetime import datetime
from sabelotodo.models import Item, ItemSchema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from .helpers import populate
from .testdata import VALID_ITEM_DATA, ADDITIONAL_VALID_ITEM_DATA, \
        INVALID_ITEM_DATA

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@pytest.mark.parametrize("data", VALID_ITEM_DATA)
def test_create_item(_db, data):
    """ When a new Item is created, the fields are set
    correctly. """
    item = item_schema.load(data)
    for k in data:
        v = getattr(item, k)
        if isinstance(v, datetime):
            assert datetime.strptime(data[k], "%a, %d %b %y %H:%M:%S -0000") == v
        else:
            assert data[k] == v


@pytest.mark.parametrize("data", ADDITIONAL_VALID_ITEM_DATA)
def test_item_can_be_committed(_db, data):
    """ An item can be added directly to a populated database. """

    populate(_db, items_schema, VALID_ITEM_DATA)
    item = item_schema.load(data)

    before = Item.query.all()
    _db.session.add(item)
    _db.session.commit()
    after = Item.query.all()

    created = [i for i in after if i not in before]
    assert created == [item], "Only the specified item is created."


@pytest.mark.parametrize("data", INVALID_ITEM_DATA)
def test_invalid_data_is_rejected(_db, data):
    """ Creating an item with invalid data raises an error at the level of the
    schema. """
    with pytest.raises(ValidationError):
        item_schema.load(data)
