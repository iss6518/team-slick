''' test_interface.py will store all of the tests for our interface'''
import pytest
import db.interface as wrld


@pytest.fixture(scope='function')
def temp_user():
    name = wrld._get_test_name()
    ret = wrld.add_user(name, 1, "gender", "interest")
    yield name
    if wrld.exists(name):
        wrld.del_user(name)



def test_get_test_name():
    name = wrld._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = wrld._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == wrld.ID_LEN


def test_get_test_user():
    assert isinstance(wrld.get_test_user(), dict)


def test_get_users(temp_user):
    users = wrld.fetch_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    assert wrld.exists(temp_user)


def test_add_user_dup_name(temp_user):
    """
    Making sure a duplicate user name raises a value error
    """
    dup_name = temp_user
    with pytest.raises(ValueError):
        wrld.add_user(dup_name, 1, "gender", "interest")



ADD_USER = "New User"


def test_add_user():
    new_name = wrld._get_test_name()
    ret = wrld.add_user(new_name, 30, "Female", "hiking")
    assert wrld.exists(new_name)
    assert isinstance(ret, bool)
    wrld.del_user(new_name)


def test_del_user(temp_user):
    name = temp_user
    wrld.del_user(name)
    assert not wrld.exists(name)


def test_del_user_not_there():
    name = wrld._get_test_name()
    with pytest.raises(ValueError):
        wrld.del_user(name)



