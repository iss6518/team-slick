import db.users as testUsers
import pytest


def test_get_users():
    users = testUsers.fetch_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= testUsers.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert testUsers.INTERESTS in user
        assert isinstance(user[testUsers.INTERESTS], list)


def test_get_friend_requests():
    friendRequests = testUsers.get_friend_requests()
    assert isinstance(friendRequests, dict)
    for key in friendRequests:
        assert isinstance(key, str)
        friendRequest = friendRequests[key]
        assert isinstance(friendRequest, dict)


def test_add_friend():
    adding_friend = testUsers.add_friend(testUsers.USER_NAME)
    assert isinstance(adding_friend, dict)
    added_friend = adding_friend[testUsers.USER_NAME]
    assert testUsers.USER_NAME in testUsers.my_friends.keys()


def test_duplicate_friend():
    name = testUsers.TESTNAME
    with pytest.raises(ValueError):
        testUsers.add_friend(name)