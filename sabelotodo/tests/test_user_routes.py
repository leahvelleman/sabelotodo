import pytest
from sabelotodo.models import User, UserSchema
from .testdata import VALID_USER_DATA, INVALID_USER_DATA

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def test_user_route_with_multiple_users(test_client, _db):
    """ The /user route retrieves all users added. """

    users = users_schema.load(VALID_USER_DATA)
    _db.session.add_all(users)
    _db.session.commit()

    return_value = test_client.get('/user')
    returned_users = users_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert returned_users == User.query.all(), "Returned users match database."
