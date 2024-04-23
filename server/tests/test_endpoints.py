from http.client import OK, NOT_FOUND, FORBIDDEN, NOT_ACCEPTABLE, BAD_REQUEST

from unittest.mock import patch

import pytest

import forms.form_filler as ff

import server.endpoints as ep

import db.users as users

import db.interface as interface

TEST_CLIENT = ep.app.test_client()

mockName = "Dareck"
mockAge = 28
mockGender = "female"
mockInterests = "running"
mockEmail = "test@gmail.com"
mockPassword = "password"
mockValues = {users.NAME: mockName, users.AGE: mockAge, users.GENDER: mockGender, users.INTERESTS: mockInterests, users.EMAIL: mockEmail, users.PASSWORD: mockPassword}

mock2Name = "Dareck"
mockOtherName = "John"
mockMatchValues = {interface.NAME: mock2Name, interface.OTHER_USER: mockOtherName}

mock3Name = users.get_test_user()
mock2OtherName = users.get_test_user()
mock_CoupleValues = {interface.NAME: mock3Name, interface.OTHER_USER: mock2OtherName}


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


# TESTS FOR USER
# test for adding user
@patch('db.users.add_user', side_effect=ValueError(), autospec=True)
def test_for_users_bad_add(mock_add):
    resp = TEST_CLIENT.post(ep.USERS_EP, json=users.get_test_user())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.users.add_user', return_value=True, autospec=True)
def test_users_add(mock_add):
    """
    Testing we do the right thing with a good return from add_game.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=users.get_test_user())
    assert resp.status_code == OK


# test for updating user
@patch('db.users.update_user', side_effect=ValueError(), autospec=True)
def test_for_users_bad_update(mock_add):
    resp = TEST_CLIENT.put(ep.USERS_EP, json=mockValues)
    assert resp.status_code == NOT_ACCEPTABLE
 

@patch('db.users.update_user', return_value=True, autospec=True)
def test_update_user_success(mock_add):
    """
    Testing we do the right thing with a good return from update_user.
    """
    resp = TEST_CLIENT.put(ep.USERS_EP, json=mockValues)
    assert resp.status_code == OK


# test for deleting user
@patch('db.users.del_user', return_value = True, autospec=True)
def test_user_del(mock_del):
    """
    Testing we do the right thing with a call to del_user that succeeds
    """
    resp = TEST_CLIENT.delete(ep.USERS_EP, json = mockValues)
    assert resp.status_code == OK


@patch('db.users.del_user', side_effect = ValueError(), autospec=True)
def test_user_bad_del(mock_del):
   """
    Testing we do the right thing with a value error from  del_user
    """
   resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/AnyName')
   assert resp.status_code == NOT_FOUND


# a skip test
@pytest.mark.skip('An example of using skip for a failing test' 
            + ' until it is dealt with at a later time' )
def test_that_doesnt_work():
    assert False


# TESTS FOR MATCHING
# test for getting all matches in db
def test_return_matches():
    resp = TEST_CLIENT.get(ep.MATCHES_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.DATA in resp_json


# test for unmatching users
@patch('db.interface.unmatch_users', return_value=True, autospec=True)
def test_unmatch_users_success(mock_add):
    resp = TEST_CLIENT.delete(ep.MATCHES_EP, json=mockMatchValues)
    assert resp.status_code == OK


@patch('db.interface.unmatch_users', side_effect=ValueError(), autospec=True)
def test_for_users_bad_unmatch(mock_add):
    resp = TEST_CLIENT.delete(ep.MATCHES_EP, json=mockMatchValues)
    assert resp.status_code == NOT_ACCEPTABLE
 

# test for matching users
@patch('db.interface.match_users', return_value=True, autospec=True)
def test_match_users_success(mock_add):
    resp = TEST_CLIENT.post(ep.MATCHES_EP, json=mockMatchValues)
    assert resp.status_code == OK


@patch('db.interface.match_users', side_effect=ValueError(), autospec=True)
def test_for_users_bad_match(mock_add):
    resp = TEST_CLIENT.post(ep.MATCHES_EP, json=mockMatchValues)
    assert resp.status_code == NOT_ACCEPTABLE


# TESTS FOR FRIEND REQUEST
# @patch('db.interface.acceptFriendReq',return_value = True, autospec=True)
# def test_acceptReq(mock_add):
#     """
#     Testing we do the right thing with a call to acceptFriendReq that succeeds
#     """
#     resp = TEST_CLIENT.put(ep.FRIENDREQ_EP, json = mock_CoupleValues)
#     assert resp.status_code == OK


# test for accepting (updating) friend request
@patch('db.interface.acceptFriendReq', side_effect=ValueError(), autospec=True)
def bad_test_acceptReq(mock_add):
    resp = TEST_CLIENT.put(ep.FRIENDREQ_EP, json = mock_CoupleValues)
    assert resp.status_code == NOT_ACCEPTABLE


@patch('db.interface.update_match',return_value = True, autospec=True)
def test_update_match(mock):
    resp = TEST_CLIENT.put(ep.MATCHES_EP, json = mock_CoupleValues)
    assert resp.status_code == OK


@patch('db.interface.update_match', side_effect=ValueError(), autospec=True)
def bad_test_update_match(mock):
    resp = TEST_CLIENT.put(ep.MATCHES_EP, json = mock_CoupleValues)
    assert resp.status_code == NOT_ACCEPTABLE
