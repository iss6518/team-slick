# interface for our user data
import random

# import db.db_connect as dbc
# USERS_COLLECT = "users"

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

INTERESTS = 'interests'
NAME = 'user_name'
GENDER = ''
AGE = 22
TEST_USER_NAME = 'WILL'

users = {}
"""
users = {
    'John': {
        AGE: 22,

    },

    TEST_USER_NAME: {
        AGE: 25
    },

}
"""


def _get_test_name():
    """
    Function to get the random test user name
    """
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_user():
    """
    Function to return us a sample test user
    """
    test_user = {}
    test_user[NAME] = _get_test_name()
    test_user[AGE] = 18
    return test_user


def del_user(name: str):
    """
    A function to remove a user from list of users
    """
    if name in users:
        del users[name]
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def fetch_users() -> dict:
    """
    A function to return all users in the data store.
    """
    return users


def exists(name: str) -> bool:
    """
    Function to check if user exists, returns bool
    """
    return name in fetch_users()


def _gen_id() -> str:
    """
    Function to produce ID for users
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_user(name: str, age: int, gender: str, interest: str) -> str:
    """
    Function to add users. For interests, users only enter 1 interest
    """
    if name in users:
        raise ValueError(f'Duplicate user name: {name= }')
    if not name:
        raise ValueError("User can't be blank")

    # code for adding a user to mongodb as appose to local memory
    # TODO: this code brings up a lot of errors in test_interface.py so
    # commenting out now until class next week
    # user = {}
    # user = {NAME: name, AGE: age, GENDER: gender, INTERESTS: interest}
    # dbc.connect_db()
    # _id = dbc.insert_one(USERS_COLLECT, user)
    # return _id is not None

    users[name] = {AGE: age, GENDER: gender, INTERESTS: interest}
    return _gen_id()
