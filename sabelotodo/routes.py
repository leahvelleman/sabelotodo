from flask import current_app as app
from .models import Item
from flask import jsonify
from dataclasses import asdict


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item')
def all_items():
    return jsonify([asdict(i) for i in Item.query.all()])


if __name__ == '__main__':
    app.run()