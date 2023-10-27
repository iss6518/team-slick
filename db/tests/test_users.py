import db.users as testUsers


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
