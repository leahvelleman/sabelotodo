import pytest
from sabelotodo.models import User, UserSchema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from .helpers import populate
from .testdata import VALID_USER_DATA, INVALID_USER_DATA

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_create_user(_db, data):
    """ When a new User is created, the username and email fields
    are set correctly. """
    user = User(**data)
    assert user.username == data['username']
    assert user.email == data['email']


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_cannot_serialize_password(_db, data):
    """ When a User is serialized, the password field is omitted. """
    user = User(**data)
    userdict = user_schema.dump(user)
    assert 'password' not in userdict


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_is_stored_hashed(_db, data):
    """ The stored value for a password isn't the plaintext password. """
    user = User(**data)
    assert user.check_password(data['password'])
    assert user.password != data['password']


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_can_be_checked(_db, data):
    """ Checking with the correct password returns True. """
    user = User(**data)
    assert user.check_password(data['password'])


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_password_can_be_changed(_db, data):
    """ Changing a password makes the new one work and not the old one. """
    user = User(**data)
    newpassword = "asdk98*(23f!N"
    user.set_password(newpassword)
    assert user.check_password(newpassword)
    assert not user.check_password(data['password'])


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_user_can_be_committed(_db, data):
    """ A valid user can be committed to the database. """
    user = User(**data)
    _db.session.add(user)
    _db.session.commit()
    assert User.query.get(user.id) == user


@pytest.mark.parametrize("data", VALID_USER_DATA)
def test_duplicate_username_is_rejected(_db, data):
    """ Adding a user whose username is already in the database raises
    an SQLAlchemy error. Routes will need to test for this to produce
    a friendly http error code instead. """
    populate(_db, User, VALID_USER_DATA)

    with pytest.raises(IntegrityError):
        new_user = User(**data)
        _db.session.add(new_user)
        _db.session.commit()
    _db.session.rollback()


@pytest.mark.parametrize("data", INVALID_USER_DATA)
def test_invalid_data_is_rejected(_db, data):
    """ Creating a user with invalid data raises an error at the level of the
    schema. """
    with pytest.raises(ValidationError):
        user_schema.load(data)
