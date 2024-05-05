''' test_interface.py will store all of the tests for our interface'''
import pytest
import db.interface as wrld
import db.users as users
import forms.form_filler as ff

# test for match_ep db functions
def test_match_users():
    new_name = users._get_test_name()
    ret1 = users.add_user(new_name, 30, "Female", "hiking", "test@gmail.com", "password")
    new_name2 = users._get_test_name()
    ret2 = users.add_user(new_name2, 30, "Female", "hiking", "test@gmail.com", "password")

    matching = wrld.newMatchUsers(new_name, new_name2)
    # assert wrld.match_exists(IDTuple[0])
    # assert wrld.match_exists(IDTuple[1])
    assert isinstance(matching, bool)
    wrld.unmatch_users(new_name, new_name2)
    users.del_user(new_name)
    users.del_user(new_name2)


def test_unmatch_users():
    #match test users
    new_name1 = users._get_test_name()
    ret = users.add_user(new_name1, 30, "Female", "Hiking", "test@gmail.com", "password")
    new_name2 = users._get_test_name()
    ret = users.add_user(new_name2, 30, "Female", "Hiking", "test@gmail.com", "password")
    wrld.newMatchUsers(new_name1, new_name2)
    #unmatching
    unmatching = wrld.unmatch_users(new_name1, new_name2)
    assert isinstance(unmatching, bool)
    users.del_user(new_name1)
    users.del_user(new_name2)


def test_fetch_matches():
    sample_dict = wrld.fetch_matches()
    dictlen = len(sample_dict)
    assert dictlen >= 0
    assert isinstance(sample_dict, dict)


# test for friend request db functions
def test_fetch_friendReqs():
    dictlen = len(wrld.fetch_friendReqs())
    assert dictlen >= 0


def test_acceptFriendReq():
    new_name1 = users._get_test_name()
    ret1 = users.add_user(new_name1, 30, "Female", "hiking", "test@gmail.com", "password")
    new_name2 = users._get_test_name()
    ret2 = users.add_user(new_name2, 30, "Female", "hiking", "test@gmail.com", "password")
    testbool = wrld.acceptFriendReq(new_name1, new_name2)
    assert isinstance(testbool, bool)
    wrld.unmatch_users(new_name1, new_name2)
    users.del_user(new_name1)
    users.del_user(new_name2)


def test_deleteFriendReq():
    new_name = users._get_test_name()
    ret1 = users.add_user(new_name, 30, "Female", "hiking", "test@gmail.com", "password")
    friendreqs = wrld.fetch_friendReqs()
    new_name2 = users._get_test_name()
    ret = users.add_user(new_name2, 30, "Female", "Hiking", "test@gmail.com", "password")
    success = wrld.deleteFriendReq(new_name, new_name2)
    for user in friendreqs:
        if (user == new_name):
            assert isinstance(friendreqs[new_name], dict)
    users.del_user(new_name)
    users.del_user(new_name2)


def test_sendFriendReq():
    new_name = users._get_test_name()
    ret = users.add_user(new_name, 30, "Female", "Hiking", "test@gmail.com", "password")
    new_name2 = users._get_test_name()
    ret = users.add_user(new_name2, 30, "Female", "Hiking", "test@gmail.com", "password")
    # success = wrld.sendFriendReq(new_name, new_name2)
    success = wrld.newSendFriendReq(new_name, new_name2)
    assert isinstance (success, bool)
    wrld.deleteFriendReq(new_name, new_name2)
    users.del_user(new_name)
    users.del_user(new_name2)
