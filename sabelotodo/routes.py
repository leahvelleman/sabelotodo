from flask import abort, jsonify, current_app as app
from .models import Item
from dataclasses import asdict


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item')
def all_items():
    return jsonify([asdict(i) for i in Item.query.all()])


@app.route('/item/<itemid>')
def item_by_id(itemid):
    if itemid.isnumeric():
        return_value = Item.query.get(itemid)
        if return_value:
            return asdict(rv)
    abort(404)


if __name__ == '__main__':
    app.run()
