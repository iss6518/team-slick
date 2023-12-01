# interface for our user data
import random

import db.db_connect as dbc
USERS_COLLECT = "users"

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

NAME = 'user_name'
AGE = 'age'
GENDER = 'gender'
INTERESTS = 'interests'
# TEST_USER_NAME = 'WILL'

users = {}
user_connections = {}

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
    test_user[GENDER] = "male"
    test_user[INTERESTS] = "hiking"
    return test_user


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {NAME: name})
    # return name in fetch_users()


def del_user(name: str):
    """
    A function to remove a user from list of users
    """
    if exists(name):
        return dbc.del_one(USERS_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def fetch_users() -> dict:
    """
    A function to return all users in the data store.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, USERS_COLLECT)


def _gen_id() -> str:
    """
    Function to produce ID for users
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_user(name: str, age: int, gender: str, interest: str) -> bool:
    """
    Function to add users. For interests, users only enter 1 interest
    """
    if exists(name):
        raise ValueError(f'Duplicate user name: {name= }')
    if not name:
        raise ValueError("User can't be blank")

    # code for adding a user to mongodb as appose to local memory
    # TODO: this code brings up a lot of errors in test_interface.py so
    # commenting out now until class next week
    user = {}
    user[NAME] = name
    user[AGE] = age
    user[GENDER] = gender
    user[INTERESTS] = interest

    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user)
    return _id is not None

    # users[name] = {AGE: age, GENDER: gender, INTERESTS: interest}
    # return _gen_id()


def update_user(name: str, newValues: dict) -> bool:
    """
    Function to update users (depending on field we want to change)
    """
    if not name:
        raise ValueError("User can't be blank")

    # currUserDict = dbc.fetch_one(USERS_COLLECT, {NAME: name})
    # filter = {age: 12, gender: male}
    """for key in filter:
        currUserDict[key] = filter[key]"""

    filter = {NAME: name}
    setValues = {"$set": newValues}

    dbc.connect_db()
    _id = dbc.update_one(USERS_COLLECT, filter, setValues)
    return _id is not None


# dummy function to unmatch users. Eventually update to connect with mongodb
def unmatch_users(name: str, other_user_name: str):
    """
    Unmatches two users by removing their connection.
    """
    if name not in user_connections or other_user_name not in user_connections:
        raise ValueError('User not found')

    # Remove the match for name
    if other_user_name in user_connections[name]:
        user_connections[name].remove(other_user_name)
    else:
        raise ValueError('Users are not matched')

    # Remove the match for other_user_name
    if name in user_connections[other_user_name]:
        user_connections[other_user_name].remove(name)
    else:
        raise ValueError('Users are no longer matched')
