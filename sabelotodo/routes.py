from flask import request, current_app as app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from .models import Item, ItemSchema, db

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item', methods=["GET"])
def all_items():
    return items_schema.dumps(Item.query.all())


@app.route('/item/<int:itemid>')
def get_item_by_id(itemid):
    item = Item.query.get_or_404(itemid)
    return item_schema.dumps(item)


@app.route('/item/<int:itemid>', methods=["DELETE"])
def delete_item_by_id(itemid: str):
    item = Item.query.get_or_404(itemid)
    db.session.delete(item)
    db.session.commit()
    return item_schema.dumps(item), 200


@app.route('/item', methods=["POST"])
def create_item():
    json_data = request.get_json()
    if not json_data:
        return "No data provided", 400

    try:
        item = item_schema.load(json_data)
    except ValidationError:
        return "JSON provided doesn't match schema", 400

    try:
        db.session.add(item)
        db.session.commit()
    except SQLAlchemyError:
        # TODO: This branch of code is currently untested (lbv)
        db.session.rollback()
        return "Database error", 500

    return item_schema.dumps(item), 200


@app.route('/item/<int:itemid>', methods=["PATCH"])
def patch_item(itemid):
    item = Item.query.get_or_404(itemid)
    json_data = request.get_json()

    if not json_data:
        return "No data provided", 400

    item_data = item_schema.dump(item)
    item_data.update(json_data)

    try:
        print(item_data)
        item_schema.load(item_data)
        for k, v in item_data.items():
            setattr(item, k, v)
    except ValidationError as v:
        return "JSON provided doesn't match schema when combined with specified item: %s" % v, 400

    try:
        db.session.commit()
    except SQLAlchemyError:
        # TODO: This branch of code is currently untested (lbv)
        db.session.rollback()
        return "Database error", 500

    return item_schema.dumps(item), 200


if __name__ == '__main__':
    app.run()
