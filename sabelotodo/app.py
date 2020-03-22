from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

db = SQLAlchemy(app)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/item')
def all_items():
    return jsonify([i.to_dict() for i in Item.query.all()])


if __name__ == '__main__':
    app.run()
