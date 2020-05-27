import os
import pytest
import sqlalchemy as sa
from pytest_postgresql.factories import DatabaseJanitor
from sabelotodo import create_app, db


# Retrieve a database connection string from the shell environment
try:
    DB_CONN = os.environ['TEST_DATABASE_URI']
except KeyError:
    raise KeyError('TEST_DATABASE_URI not found. You must export a database ' +
                   'connection string to the environmental variable ' +
                   'TEST_DATABASE_URI in order to run tests.')
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
    pg_user = os.environ.get('DB_USER') or 'postgres'
    pg_pass = os.environ.get('DB_PASSWORD')
    pg_db = os.environ.get('TEST_DATABASE_NAME')

    janitor = DatabaseJanitor(user=pg_user,
                              port=pg_port,
                              host=pg_host,
                              db_name=pg_db,
                              version=11.7,
                              password=pg_pass)
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


@pytest.fixture(scope='function')
def _db(app, request):
    '''
    Provide the transactional fixtures with access to the database via a
    Flask-SQLAlchemy database connection. `scope='function'` means the tables
    are dropped after each test. To trigger this teardown behavior reliably in
    a parametrized test, the test function must have this fixture as an
    argument even if it does not need to use it explicitly in the test body.
    '''
    db.app = app
    from sabelotodo.models import Item, User  # noqa: F401
    db.create_all()
    session = db.session

    @request.addfinalizer
    def clear_data():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            session.execute(table.delete())
        session.commit()

    return db


@pytest.fixture
def test_client(app):
    with app.test_client() as client:
        yield client
