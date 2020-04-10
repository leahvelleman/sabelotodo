import pytest
import random
import string
from sabelotodo.models import User, UserSchema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

user_schema = UserSchema()
users_schema = UserSchema(many=True)


VALID_USER_DATA = [
        {'username': 'leahvelleman',
         'email': 'leahvelleman@gmail.com',
         'password': 'zooblefart'},
        {'username': 'accéntedchãraçtérs',
         'email': 'fancyletters@foo.com',
         'password': '2r039fjaio'},
        {'username': 'someoneelse',
         'email': 'someone.else@gmail.com',
         'password': 'squeedleblorf'},
        {'username': 'FredNull',
         'email': 'fnull@example.com',
         'password': 'wo239u3hofwasf'},
        {'username': '도윤김',
         'email': 'doyeonkim@gmail.com',
         'password': '2398rhfeoriaselfjwe'},
        {'username': 'ExtendedUnicodePassword',
         'email': 'somuchunicode@gmail.com',
         'password': '表ポあA鷗ŒéＢ逍Üßªąñ丂㐀𠀀'},
         ]

INVALID_USER_DATA = [
        {'username': '',
         'email': 'no.username@gmail.com',
         'password': 'zooblefart'},
        {'username': '💕 💞 💓 💗 💖',
         'email': 'shmoopybutt@gmail.com',
         'password': '28hfiaslawe'},
        {'username': 'No Email',
         'email': None,
         'password': 'squeedleblorf'},
        {'username': 123,
         'email': 'username.is.the.wrong.type@hotmail.com',
         'password': '2aeaica'},
        {'username': 'Extra fields',
         'email': 'foo@foo.com',
         'useless': 'this is bad',
         'password': 'squeedleblorf'},
         ]


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_create_user(_db, data):
    """ When a new User is created, the username and email fields
    are set correctly. """
    user = user_schema.load(data)
    assert user.username == data['username']
    assert user.email == data['email']


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_cannot_serialize_password(_db, data):
    """ When a User is serialized, the password field is omitted. """
    user = user_schema.load(data)
    userdict = user_schema.dump(user)
    assert 'password' not in userdict


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_is_stored_hashed(_db, data):
    """ The stored value for a password isn't the plaintext password. """
    user = user_schema.load(data)
    assert user.password != data['password']


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_can_be_checked(_db, data):
    """ Checking with the correct password returns True. """
    user = user_schema.load(data)
    assert user.check_password(data['password'])


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_can_be_changed(_db, data):
    """ Changing a password makes the new one work and not the old one. """
    user = user_schema.load(data)
    random_string = "".join(random.choice(string.ascii_letters) for i in
                            range(30))
    user.set_password(random_string)
    assert user.check_password(random_string)
    assert not user.check_password(data['password'])


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_user_can_be_committed(_db, data):
    """ A valid user can be committed to the database. """
    user = user_schema.load(data)
    _db.session.add(user)
    _db.session.commit()
    assert User.query.get(user.id) == user


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_duplicate_username_is_rejected(_db, data):
    """ Adding a user whose username is already in the database raises
    an SQLAlchemy error. Routes will need to test for this to produce
    a friendly http error code instead. """
    users = users_schema.load(VALID_USER_DATA)
    _db.session.add_all(users)
    _db.session.commit()

    with pytest.raises(IntegrityError):
        new_user = user_schema.load(data)
        _db.session.add(new_user)
        _db.session.commit()
    _db.session.rollback()


@pytest.mark.parametrize("data", INVALID_USER_DATA)
def test_invalid_data_is_rejected(_db, data):
    """ Creating a user with invalid data raises an error at the level of the
    schema. """
    with pytest.raises(ValidationError):
        user_schema.load(data)

