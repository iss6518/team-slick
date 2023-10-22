"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

INTERESTS = 'interests'


def fetch_users():
    """
    A function to return all users in the data store.
    """
    return {
        "John": {INTERESTS: ["sports", "studying"]},
        "Will": {INTERESTS: ["music", "dance"]},
        "James": {INTERESTS: ["coffee", "cooking"]}
    }
