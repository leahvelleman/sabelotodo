from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress a warning message
db = SQLAlchemy(app)

from models import Item

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
