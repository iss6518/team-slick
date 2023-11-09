''' test_interface.py will store all of the tests for our interface'''
import pytest
import db.interface as wrld

"""
@pytest.fixture(scope='function')
def temp_user():
    name = wrld._get_test_name()
    ret = wrld.add_friend(name)
    yield name
    if wrld.exists(name):
        wrld.del_user(name)
        
        """