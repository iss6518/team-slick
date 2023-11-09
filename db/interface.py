# interface for our user data
import random

BIG_NUM = 100000000

INTERESTS = 'interests'
NAME = 'user_name'
GENDER = ''
AGE = 22
TEST_USER_NAME = 'WILL'

users = {
    'John': {
        AGE: 22,

    },

    TEST_USER_NAME: {
        AGE: 25
    },

}


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
