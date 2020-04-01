from flask import abort, jsonify, Response, current_app as app
from .models import Item, db
from dataclasses import asdict


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item')
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


if __name__ == '__main__':
    app.run()
