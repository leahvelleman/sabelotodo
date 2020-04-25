from flask import request, current_app as app
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from .models import Item, ItemSchema, User, UserSchema, db

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return "Validation error: %s" % error, 400


@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    db.session.rollback()
    return "Database error: %s" % error, 500


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


@app.route('/user/<int:userid>')
def get_user_by_id(userid):
    user = User.query.get_or_404(userid)
    return user_schema.dumps(user)


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

    item = Item(**json_data)
    db.session.add(item)
    db.session.commit()
    return item_schema.dumps(item), 200


@app.route('/item/<int:itemid>', methods=["PATCH"])
def patch_item(itemid):
    item = Item.query.get_or_404(itemid)
    json_data = request.get_json()
    if not json_data:
        return "No data provided", 400
    if "id" in json_data:
        return "ID numbers shouldn't change", 400

    update = item_schema.load(json_data, instance=item, partial=True)
    for k, v in update.items():
        setattr(item, k, v)
    db.session.commit()
    return item_schema.dumps(item), 200




if __name__ == '__main__':
    app.run()
