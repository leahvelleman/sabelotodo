import pytest

from .testdata import VALID_USER_DATA

from sabelotodo.models import User, UserSchema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


def test_user_route_can_return_all_users(test_client, _db):
    """ The /user route retrieves all users. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    return_value = test_client.get('/user')
    return_dicts = users_schema.loads(return_value.data, partial=True)

    assert return_value.status_code == 200, "The request succeeds"
    assert len(return_dicts) == len(VALID_USER_DATA), \
        "We get the number of records we expect"
    assert return_dicts[0]['username'] == VALID_USER_DATA[0]['username'], \
        "We get at least one correct username"
    assert return_dicts[0]['email'] == VALID_USER_DATA[0]['email'], \
        "We get at least one correct email"


def test_user_route_does_not_expose_passwords(test_client, _db):
    """ The /user route does not return JSON with any password fields. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    return_value = test_client.get('/user')
    return_dicts = users_schema.loads(return_value.data, partial=True)

    assert all('password' not in dict for dict in return_dicts), \
        "None of the returned JSON contains a password"


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_user_route_can_return_one_user(test_client, _db, idx):
    """ The /user route can return a single user by ID. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    return_value = test_client.get('/user/%s' % selection.id)
    return_dict = user_schema.loads(return_value.data, partial=True)

    assert return_value.status_code == 200, "The request succeeds."
    assert return_dict['username'] == selection.username, \
        "The username is correct"
    assert return_dict['email'] == selection.email, \
        "The email is correct"


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_user_route_can_delete_one_user(test_client, _db, idx):
    """ The /user/ route can delete a single user by ID. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    return_value = test_client.delete('/user/%s' % selection.id)

    assert return_value.status_code == 200, "The request succeeds."
    assert selection not in User.query.all(), "The deleted user is gone."


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_user_route_deleted_user_is_returned(test_client, _db, idx):
    """ The deleted user is returned. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    return_value = test_client.delete('/user/%s' % selection.id)
    return_dict = user_schema.loads(return_value.data, partial=True)

    assert return_dict['username'] == selection.username, \
        "Returned username matches selected user"
    assert return_dict['email'] == selection.email, \
        "Returned email matches selected user"


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_user_route_can_patch_one_user_username(test_client, _db, idx):
    """ The /user/ route can update a single username by ID. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    email = selection.email
    userid = selection.id
    password = selection.password
    return_value = test_client.patch('/user/%s' % selection.id,
                                     json={'username': 'somethingelse'})

    assert return_value.status_code == 200, "The request succeeds."
    assert selection.username == 'somethingelse', "The username changes."
    assert selection.email == email, "The email doesn't change."
    assert selection.id == userid, "The userid doesn't change."
    assert selection.password == password, "The password doesn't change."


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_user_route_patches_cannot_create_invalid_users(test_client, _db, idx):
    """ If the update would create a too-short username, it has no
    effect. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    username = selection.username
    email = selection.email
    userid = selection.id
    password = selection.password
    return_value = test_client.patch('/user/%s' % selection.id,
                                     json={'username': 'e'})

    assert return_value.status_code == 400, "The request fails nicely."
    assert selection.username == username, "The username doesn't change."
    assert selection.email == email, "The email doesn't change."
    assert selection.id == userid, "The userid doesn't change."
    assert selection.password == password, "The password doesn't change."


@pytest.mark.parametrize("idx", range(len(VALID_USER_DATA)))
def test_cannot_patch_passwords(test_client, _db, idx):

    """ If the update would change a password, it has no
    effect. """

    users = [User(**d) for d in VALID_USER_DATA]
    _db.session.add_all(users)
    _db.session.commit()

    selection = users[idx]
    username = selection.username
    email = selection.email
    userid = selection.id
    password = selection.password
    return_value = test_client.patch('/user/%s' % selection.id,
                                     json={'password': 'p@ssw0rd'})

    assert return_value.status_code == 400, "The request fails nicely."
    assert selection.username == username, "The username doesn't change."
    assert selection.email == email, "The email doesn't change."
    assert selection.id == userid, "The userid doesn't change."
    assert selection.password == password, "The password doesn't change."
