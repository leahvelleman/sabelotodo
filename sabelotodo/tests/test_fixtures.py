import json
import os
import pytest
import sqlalchemy as sa
from flask import Flask
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from pytest_postgresql.factories import DatabaseJanitor
from sabelotodo.models import Item
from sabelotodo import create_app, db


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
    pg_host = os.environ.get('DB_HOST')
    pg_port = os.environ.get('DB_PORT')
    pg_user = os.environ.get('DB_USER')
    pg_db = os.environ.get('DB_DATABASE')

    janitor = DatabaseJanitor(user=pg_user, port=pg_port, host=pg_host, db_name=pg_db, version=11.7)
    janitor.init()

    @request.addfinalizer
    def drop_database():
        janitor.drop()


class TestConfig:
    TESTING = True
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_DATABASE_URI = DB_CONN


@pytest.fixture(scope='session')
def app(database):
    '''
    Create a Flask app context for the tests.
    '''
    app = create_app(TestConfig)

    return app


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    db.app = app
    from sabelotodo.models import Item
    db.create_all()

    return db
