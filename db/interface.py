# interface for our user data
import random

import db.db_connect as dbc
USERS_COLLECT = "users"
MATCHES_COLLECT = "matches"

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

NAME = 'user_name'
AGE = 'age'
GENDER = 'gender'
INTERESTS = 'interests'
OTHER_USER = 'other_user'
ID = '_id'
FAVORITE = 'favorite'

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


def match_exists(matchID) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(MATCHES_COLLECT, {ID: matchID})


def fetch_matches() -> dict:
    """
    A function to return all matches in the data store.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(ID, MATCHES_COLLECT)


def update_match(name: str, otherName: str) -> bool:
    """
    Function to update match (depending on field we want to change)
    """
    if not name:  # TODO should use match_exits func ***
        raise ValueError("Match can't be blank")

    filter = {NAME: name, OTHER_USER: otherName}
    thisMatch = dbc.fetch_one(MATCHES_COLLECT, filter)
    setValues = {"$set": {FAVORITE: (thisMatch[FAVORITE])}}

    dbc.connect_db()
    _id = dbc.update_one(MATCHES_COLLECT, filter, setValues)
    return _id is not None


# function to unmatch users
def unmatch_users(name: str, other_user_name: str):
    """
    Unmatches two users by removing their connection.
    """
    if (not exists(name)) or (not exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Remove the match for name
    dbc.connect_db()
    try:
        dbc.del_one(MATCHES_COLLECT, {NAME: name, OTHER_USER: other_user_name})
        dbc.del_one(MATCHES_COLLECT, {NAME: other_user_name, OTHER_USER: name})
    except ValueError:
        raise ValueError('Users are not unmatched')


# function to match users
def match_users(name: str, other_user_name: str) -> bool:
    """
    Match two users by adding their connection.
    """
    if (not exists(name)) or (not exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Add the match for name
    dbc.connect_db()
    MATCHA = {NAME: name, OTHER_USER: other_user_name, FAVORITE: False}
    MATCHB = {NAME: other_user_name, OTHER_USER: name, FAVORITE: False}

    _id1 = dbc.insert_one(MATCHES_COLLECT, MATCHA)
    _id2 = dbc.insert_one(MATCHES_COLLECT, MATCHB)
    return _id1 is not None and _id2 is not None
