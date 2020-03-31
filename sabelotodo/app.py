from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import asdict
import os
from sabelotodo.models import Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

db = SQLAlchemy(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/item')
def all_items():
    return jsonify([asdict(i) for i in Item.query.all()])


if __name__ == '__main__':
    app.run()
