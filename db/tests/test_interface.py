''' test_interface.py will store all of the tests for our interface'''
import pytest
import db.interface as wrld

"""
@pytest.fixture(scope='function')
def temp_user():
    name = wrld._get_test_name()
    ret = wrld.add(name)
    yield name
    if wrld.exists(name):
        wrld.del_user(name)
        
"""

def test_gen_id():
    _id = wrld._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == wrld.ID_LEN


ADD_USER = "New User"


def test_add_user():
    ret = wrld.add_user(ADD_USER, 30, "Female", "hiking")
    assert wrld.exists(ADD_USER)
    assert isinstance(ret, str)


