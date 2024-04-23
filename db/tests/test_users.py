import db.users as testUsers
import pytest


@pytest.fixture(scope='function')
def temp_user():
    name = testUsers._get_test_name()
    ret = testUsers.add_user(name, 1, "gender", "interest", "email@gmail.com", "password")
    yield name
    if testUsers.exists(name):
        testUsers.del_user(name)


def test_get_test_name():
    name = testUsers._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = testUsers._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == testUsers.ID_LEN


def test_get_test_user():
    assert isinstance(testUsers.get_test_user(), dict)


# tests for users_ep db functions
def test_get_users(temp_user):
    users = testUsers.fetch_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    assert testUsers.exists(temp_user)


def test_add_user_dup_name(temp_user):
    """
    Making sure a duplicate user name raises a value error
    """
    dup_name = temp_user
    with pytest.raises(ValueError):
        testUsers.add_user(dup_name, 1, "gender", "interest", "email@gmail.com", "password")


def test_add_user():
    new_name = testUsers._get_test_name()
    ret = testUsers.add_user(new_name, 30, "Female", "hiking", "test@gmail.com", "password")
    assert testUsers.exists(new_name)
    assert isinstance(ret, bool)
    testUsers.del_user(new_name)


def test_del_user(temp_user):
    name = temp_user
    testUsers.del_user(name)
    assert not testUsers.exists(name)


def test_del_user_not_there():
    name = testUsers._get_test_name()
    with pytest.raises(ValueError):
        testUsers.del_user(name)


def test_update_user():
    new_name = testUsers._get_test_name()
    ret = testUsers.add_user(new_name, 30, "Female", "hiking", "test@gmail.com", "password")
    testUsers.update_user(new_name, {testUsers.AGE: 27, testUsers.GENDER: "male"})
    assert testUsers.exists(new_name)
    assert isinstance(ret, bool)
    testUsers.del_user(new_name)
