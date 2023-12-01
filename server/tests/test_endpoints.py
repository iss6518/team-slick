from http.client import OK, NOT_FOUND, FORBIDDEN, NOT_ACCEPTABLE, BAD_REQUEST

from unittest.mock import patch

import pytest

import db.users as users

import server.endpoints as ep
import db.interface as interface

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.DATA in resp_json

@patch('db.interface.add_user', side_effect=ValueError(), autospec=True)
def test_for_users_bad_add(mock_add):
    resp = TEST_CLIENT.post(ep.INTERFACE_EP, json=interface.get_test_user())
    assert resp.status_code == NOT_ACCEPTABLE
    
@patch('db.interface.add_user', return_value=True, autospec=True)
def test_users_add(mock_add):
    """
    Testing we do the right thing with a good return from add_game.
    """
    resp = TEST_CLIENT.post(ep.INTERFACE_EP, json=interface.get_test_user())
    assert resp.status_code == OK

@pytest.mark.skip('An example of using skip for a failing test' 
            + ' until it is dealt with at a later time' )
def test_that_doesnt_work():
    assert False

mockName = "Dareck"
mockAge = 28
mockGender = "female"
mockInterests = "running"

mockValues = {interface.NAME: mockName, interface.AGE: mockAge, interface.GENDER: mockGender, interface.INTERESTS: mockInterests}

@patch('db.interface.update_user', side_effect=ValueError(), autospec=True)
def test_for_users_bad_update(mock_add):
    resp = TEST_CLIENT.put(ep.INTERFACE_EP, json=mockValues)
    assert resp.status_code == NOT_ACCEPTABLE
    

@patch('db.interface.update_user', return_value=True, autospec=True)
def test_update_user_success(mock_add):
    """
    Testing we do the right thing with a good return from update_user.
    """
    resp = TEST_CLIENT.put(ep.INTERFACE_EP, json=mockValues)
    assert resp.status_code == OK


@patch('db.interface.unmatch_users', return_value=True, autospec=True)
def test_for_users_unmatch_users_success(mock_add):
    resp = TEST_CLIENT.put(ep.INTERFACE_EP, json=mockValues)
    assert resp.status_code == OK


# # "Skeleton of patches for our del_user function"
# #
# #@patch('db.users.del_user', autospec=True)
# #def test_user_del(mock_del):
# #    """
# #    Testing we do the right thing with a call to del_user that succeeds
# #    """
# #    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/AnyName')
# #    assert resp.status_code == OK
# #    
# #    
# #@patch('db.users.del_user', side_effect = ValueError(), autospec=True)
# #def test_user_bad_del(mock_del):
# #    """
# #    Testing we do the right thing with a value error from  del_user
# #    """
# #    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/AnyName')
# #    assert resp.status_code == NOT_FOUND
