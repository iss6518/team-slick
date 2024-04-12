# interface for matching and sending friend requests for our users
import random

import forms.form_filler as ff

import db.db_connect as dbc

USERS_COLLECT = "users"

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

ID = '_id'
NAME = 'user_name'
AGE = 'age'
GENDER = 'gender'
INTERESTS = 'interests'

FLD_NM = 'fld_nm'


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


def _gen_id() -> str:
    """
    Function to produce ID for users
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


# FOR USERS
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


def search_user(name: str) -> dict:
    """
    A function to return a specific user in the data store.
    """
    if exists(name):
        return dbc.fetch_one(USERS_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Search failure: {name} not in database.')


USERNAME = 'username'
AGE = 'age'
GENDER = 'gender'
INTEREST = 'interest'
EMAIL = 'email'
PASSWORD = 'password'

"""
Search a user (assn for 4/4/24 lecture)
QUESTION: where to add tests & return FIND_UDER_FORM_FLDS? ***
"""
FIND_USER_FORM_FLDS = [
    {
        FLD_NM: USERNAME,
        ff.QSTN: 'Enter username (not just name) to find specific user',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.INSTRUCTIONS: True,
    }
]


def add_user(name: str, age: int, gender: str, interest: str) -> bool:
    """
    Function to add users. For interests, users only enter 1 interest
    """
    if exists(name):
        raise ValueError(f'Duplicate user name: {name= }')
    if not name:
        raise ValueError("User can't be blank")

    user = {}
    user[NAME] = name
    user[AGE] = age
    user[GENDER] = gender
    user[INTERESTS] = interest

    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user)
    return _id is not None


"""
Create an account form aka Member Reg (assn for 4/4/24 lec)
QUESTION: where to add tests & return FIND_UDER_FORM_FLDS? ***
"""
CREATE_ACCOUNT_FORM_FLDS = [
    {
        FLD_NM: 'Instructions',
        ff.QSTN: 'Create an account by filling in details below',
        ff.INSTRUCTIONS: True,
    },
    {
        FLD_NM: USERNAME,
        ff.QSTN: 'Choose an username to create an account',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.INSTRUCTIONS: True,
    },
    {
        FLD_NM: AGE,
        ff.QSTN: 'Pick an age to create an account:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: GENDER,
        ff.QSTN: 'Pick a gender to create an account:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: INTEREST,
        ff.QSTN: 'Add an interest to create an account',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: EMAIL,
        ff.QSTN: 'Add your email to create an account',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: PASSWORD,
        ff.QSTN: 'Choose a password to secure your account',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
]


def update_user(name: str, newValues: dict) -> bool:
    """
    Function to update users (depending on field we want to change)
    """
    if not name:
        raise ValueError("User can't be blank")

    filter = {NAME: name}
    setValues = {"$set": newValues}

    dbc.connect_db()
    _id = dbc.update_one(USERS_COLLECT, filter, setValues)
    return _id is not None
