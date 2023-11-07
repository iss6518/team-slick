"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

INTERESTS = 'interests'
MIN_USER_NAME_LEN = 2
USER_NAME = "Will"
ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
MOCK_ID = '0' * ID_LEN

all_users = {
    "John": {INTERESTS: ["sports", "studying"]},
    "Will": {INTERESTS: ["music", "dance"]},
    "James": {INTERESTS: ["coffee", "cooking"]},
    "Mike": {INTERESTS: ["sports", "swe"]}
}

my_friends = {
    "John": {INTERESTS: ["sports", "studying"]},
}

my_friend_requests = {
    "James": {INTERESTS: ["coffee", "cooking"]},
    "Mike": {INTERESTS: ["sports", "swe"]}
}


def fetch_users() -> dict:
    """
    A function to return all users in the data store.
    """
    return all_users


def get_friend_requests() -> dict:
    """
    A function to return all of a user's friend requests
    """
    return my_friend_requests


def add_friend(user_name: str) -> dict:
    if user_name in my_friends:
        raise ValueError(f'Duplicate friend add: {user_name=}')
    my_friends[user_name] = all_users[user_name]
    return my_friends


def get_friends() -> dict:
    """
    A function to return all of a users friends
    """
    return my_friends
