import json
import os
import pytest
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest_postgresql.factories import (DatabaseJanitor,
                                         drop_postgresql_database)
from sabelotodo.models import Item, db


# Retrieve a database connection string from the shell environment
try:
    DB_CONN = os.environ['TEST_DATABASE_URL']
except KeyError:
    raise KeyError('TEST_DATABASE_URL not found. You must export a database ' +
                   'connection string to the environmental variable ' +
                   'TEST_DATABASE_URL in order to run tests.')
else:
    DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()

pytest_plugins = ['pytest-flask-sqlalchemy']

@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = "localhost"
    pg_port = "5432"
    pg_user = "postgres"
    pg_db = "sabelotodo_test"

    janitor = DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, 11.7)
    janitor.init()

    @request.addfinalizer
    def drop_database():
        janitor.drop()


@pytest.fixture(scope='session')
def app(database):
    '''
    Create a Flask app context for the tests.
    '''
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

    return app


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    db = SQLAlchemy(app=app)

    return db

@pytest.fixture(scope='module')
def item(request, _db):
    '''
    Create a table to use for updating in the process of testing direct database access.
    '''
    from sabelotodo.models import Item
    # Create tables
    _db.create_all()
    @request.addfinalizer
    def drop_tables():
        _db.drop_all()
    return Item

def test_create_item(_db, item):
    i = item(name='TestItem', order=0, done=True)
    _db.session.add(i)
    _db.session.commit()
