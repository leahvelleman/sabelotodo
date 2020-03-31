from os import environ

class Config:
    # TESTING = environ.get('TESTING')
    # FLASK_DEBUG = environ.get('FLASK_DEBUG')
    # SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
