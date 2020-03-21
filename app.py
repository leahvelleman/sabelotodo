from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_UI'] = os.environ['DATABASE_URL']


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
