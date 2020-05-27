import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from sabelotodo import create_app, db

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
