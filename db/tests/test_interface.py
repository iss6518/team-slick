''' test_interface.py will store all of the tests for our interface'''
import pytest
import db.interface as wrld


# test for match_ep db functions
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


def test_unmatch_users():
    #match test users
    new_name1 = wrld._get_test_name()
    ret = wrld.add_user(new_name1, 30, "Female", "Hiking")
    new_name2 = wrld._get_test_name()
    ret = wrld.add_user(new_name2, 30, "Female", "Hiking")
    wrld.match_users(new_name1, new_name2)
    #unmatching 
    unmatching = wrld.unmatch_users(new_name1, new_name2)
    assert not isinstance(unmatching, bool)
    wrld.del_user(new_name1)
    wrld.del_user(new_name2)


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
    new_name2 = wrld._get_test_name()
    ret = wrld.add_user(new_name2, 30, "Female", "Hiking")
    success = wrld.deleteFriendReq(new_name, new_name2)
    for user in friendreqs:
        if (user == new_name):
            assert isinstance(friendreqs[new_name], dict)
    wrld.del_user(new_name)
    wrld.del_user(new_name2)


def test_sendFriendReq():
    new_name = wrld._get_test_name()
    ret = wrld.add_user(new_name, 30, "Female", "Hiking")
    new_name2 = wrld._get_test_name()
    ret = wrld.add_user(new_name2, 30, "Female", "Hiking")
    success = wrld.sendFriendReq(new_name, new_name2)
    assert isinstance (success, bool)
    wrld.del_user(new_name)
    wrld.del_user(new_name2)
