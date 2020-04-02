from flask import abort, jsonify, request, Response, current_app as app
from .models import Item, ItemSchema, db
from dataclasses import asdict

item_schema = ItemSchema()

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item', methods=["GET"])
def all_items():
    return jsonify([asdict(i) for i in Item.query.all()])


@app.route('/item/<int:itemid>')
def get_item_by_id(itemid):
    item = Item.query.get_or_404(itemid)
    return asdict(item)


@app.route('/item/<int:itemid>', methods=["DELETE"])
def delete_item_by_id(itemid: str):
    item = Item.query.get_or_404(itemid)
    db.session.delete(item)
    db.session.commit()
    return Response(status=200)


@app.route('/item', methods=["POST"])
def create_item():
    json_data = request.get_json()
    print(json_data)
    item = item_schema.load(json_data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item), 200


if __name__ == '__main__':
    app.run()
