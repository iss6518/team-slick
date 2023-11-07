from http.client import OK, NOT_FOUND, FORBIDDEN, NOT_ACCEPTABLE, BAD_REQUEST

from unittest.mock import patch

import pytest

import db.users as users

import server.endpoints as ep

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


    @patch('db.users.add_friend', side_effect=ValueError(), autospec=True)
    def test_for_users_bad_add(mock_add):
        resp = TEST_CLIENT.post(ep.USERS_EP, json=users.fetch_users())
        assert resp.status_code == NOT_ACCEPTABLE


    @pytest.mark.skip('An example of using skip for a failing test' 
                + ' until it is dealt with at a later time' )
    def test_that_doesnt_work():
        assert False
