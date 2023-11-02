"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

INTERESTS = 'interests'
MIN_USER_NAME_LEN = 2
NAME = 'John'

users = {
        "John": {INTERESTS: ["sports", "studying"]},
        "Will": {INTERESTS: ["music", "dance"]},
        "James": {INTERESTS: ["coffee", "cooking"]}
}

friends = {
        "John": {INTERESTS: ["sports", "studying"]},
}


def fetch_users():
    """
    A function to return all users in the data store.
    """
    return users


def get_friend_requests(name):
    """
    A function to return all friend requests for user w/ provided name
    """
    return {
        "John": {INTERESTS: ["cars", "sports"]},
        "Mike": {INTERESTS: ["sports", "swe"]}
    }


def add_friend(userName: str) -> dict:
    if userName in friends:
        raise ValueError(f'Duplicate friend: {userName=}')
    friends[userName] = users[userName]
    return friends
