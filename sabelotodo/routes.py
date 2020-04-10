from flask import request, current_app as app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from .models import Item, ItemSchema, User, UserSchema, db

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


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
    if "id" in json_data:
        return "ID numbers shouldn't change", 400

    try:
        update = item_schema.load(json_data, instance=item, partial=True)
        update.id = itemid
    except ValidationError as v:
        return "JSON provided doesn't match schema when combined with specified item: %s" % v, 400

    try:
        db.session.merge(update)
        db.session.commit()
    except SQLAlchemyError as e:
        # TODO: This branch of code is currently untested (lbv)
        db.session.rollback()
        print(e)
        return "Database error", 500

    return item_schema.dumps(item), 200


@app.route('/user', methods=["GET"])
def all_users():
    return users_schema.dumps(User.query.all())


if __name__ == '__main__':
    app.run()
