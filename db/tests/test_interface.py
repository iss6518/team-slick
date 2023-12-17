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

def test_update_user():
    new_name = wrld._get_test_name()
    ret = wrld.add_user(new_name, 30, "Female", "hiking")
    wrld.update_user(new_name, {wrld.AGE: 27, wrld.GENDER: "male"})
    assert wrld.exists(new_name)
    assert isinstance(ret, bool)
    wrld.del_user(new_name)

def test_match_users():
    new_name = wrld._get_test_name()
    ret1 = wrld.add_user(new_name, 30, "Female", "hiking")
    new_name2 = wrld._get_test_name()
    ret2 = wrld.add_user(new_name2, 30, "Female", "hiking")

    matching = wrld.match_users(new_name, new_name2)
    # assert wrld.match_exists(IDTuple[0])
    # assert wrld.match_exists(IDTuple[1])
    assert isinstance(matching, bool)
    wrld.unmatch_users(new_name, new_name2)
    wrld.del_user(new_name)
    wrld.del_user(new_name2)

def test_fetch_friendReqs():
    dictlen = len(wrld.fetch_friendReqs())
    assert dictlen >= 0

def test_acceptFriendReq():
    new_name1 = wrld._get_test_name()
    ret1 = wrld.add_user(new_name1, 30, "Female", "hiking")
    new_name2 = wrld._get_test_name()
    ret2 = wrld.add_user(new_name2, 30, "Female", "hiking")
    testbool = wrld.acceptFriendReq(new_name1, new_name2)
    assert not isinstance(testbool, bool)
    wrld.unmatch_users(new_name1, new_name2)
    wrld.del_user(new_name1)
    wrld.del_user(new_name2)

def test_deleteFriendReq():
    new_name = wrld._get_test_name()
    ret1 = wrld.add_user(new_name, 30, "Female", "hiking")
    friendreqs = wrld.fetch_friendReqs()
    for user in friendreqs:
        assert isinstance(user, str)
        assert isinstance(friendreqs[user], dict)
    wrld.del_user(new_name)
    
# def test_sendFriendReq():

# def test_unmatch_users():
#     #match test users
#     new_name1 = wrld._get_test_name()
#     ret = wrld.add_user(new_name1, 30, "Female", "Hiking")
#     new_name2 = wrld._get_test_name()
#     ret = wrld.add_user(new_name1, 31, "Female", "Hiking")
#     wrld.match_users(new_name1, new_name2)
#     #unmatching 
#     unmatching = wrld.unmatch_users(new_name1, new_name2)
#     assert isinstance(unmatching, bool)
#     assert not wrld.match_exists(new_name1, new_name2)
#     #delete test users
#     wrld.del_user(new_name1)
#     wrld.del_user(new_name2)
