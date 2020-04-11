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


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_get_userid_route_with_valid_id(test_client, _db, idx):
    """ The /user/<id> route retrieves just the user with the specified ID. """

    users = users_schema.load(VALID_USER_DATA)
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    return_value = test_client.get('/user/%s' % selection.id)
    returned_user = user_schema.loads(return_value.data)

    assert return_value.status_code == 200, "The request succeeds."
    assert returned_user == selection, "We get back the user we expect."

    _db.session.rollback()  # TODO: This shouldn't be necessary, and for
    # the tests in test_routes.py it *isn't* necessary. Figure out why.
    # LV
