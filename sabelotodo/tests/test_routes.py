from sabelotodo.models import Item
from dataclasses import asdict

import json

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
    rv = test_client.get('/item')
    assert json.loads(rv.data) == []

def test_item_route_with_multiple_items(test_client, _db):
    """ Verify that the /item route retrieves all items added """
    i = Item(name="a", order=0, done=False)
    j = Item(name="b", order=2, done=True)
    k = Item(name="c", order=1, done=False)

    _db.session.add(i)
    _db.session.add(j)
    _db.session.add(k)
    _db.session.commit()

    rv = test_client.get('/item') 
    assert json.loads(rv.data) == [asdict(i) for i in Item.query.all()]

def test_itemid_route_with_valid_id(test_client, _db):
    """ Verify that the /item/<id> route retrieves just the item with the ID in
    question"""
    i = Item(name="a", order=0, done=False)
    j = Item(name="b", order=2, done=True)
    k = Item(name="c", order=1, done=False)

    _db.session.add(i)
    _db.session.add(j)
    _db.session.add(k)
    _db.session.commit()

    this_id = j.id
    rv = test_client.get('/item/%s' % this_id)
    assert json.loads(rv.data) == asdict(j)

def test_itemid_route_failures(test_client, _db):
    i = Item(name="a", order=0, done=False)
    j = Item(name="b", order=2, done=True)
    k = Item(name="c", order=1, done=False)

    _db.session.add(i)
    _db.session.add(j)
    _db.session.add(k)
    _db.session.commit()

    rv = test_client.get('/item/999')
    assert rv.status_code == 404

    rv = test_client.get('/item/-1')
    assert rv.status_code == 404

    rv = test_client.get('/item/')
    assert rv.status_code == 404

    rv = test_client.get('/item/spork')
    assert rv.status_code == 404

