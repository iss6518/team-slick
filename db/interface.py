# interface for matching and sending friend requests for our users
import db.db_connect as dbc
import db.users as users

# collections in our database
USERS_COLLECT = "users"
MATCHES_COLLECT = "matches"
FRIENDREQ_COLLECT = "friendRequests"

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

ID = '_id'
NAME = 'user_name'
OTHER_USER = 'other_user'

# lists used to keep track of friend requests
FRR = 'friend_request_received'
FRS = 'friend_request_sent'

# lists used to keep track of matches
MATCHES = 'match_list'
FAVORITES = 'favorites'


# FOR LOGIN
def login(email: str, password: str) -> dict:
    """
    A function to search db for matching email & password
    """
    dbc.connect_db()
    filter = {users.EMAIL: email, users.PASSWORD: password}
    user = dbc.fetch_one(USERS_COLLECT, filter)
    print("User:", user)
    return user


def get_authenticated_user(session):
    dbc.connect_db()
    # print(session)
    # print(session['user_id'], session['email'])
    if 'user_id' in session and 'email' in session:
        # user_id = session['user_id']
        email = session['email']
        # should also filter by _id here but need to figure out
        # how to search by _id in mongo
        filter = {users.EMAIL: email}
        user = dbc.fetch_one(USERS_COLLECT, filter)
        return user
    else:
        return None


# FOR MATCHING
def match_exists(matchID) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(MATCHES_COLLECT, {ID: matchID})


def fetch_matches() -> dict:
    """
    A function to return all matches in the data store.
    """
    dbc.connect_db()
    docs = dbc.fetch_all_as_dict(NAME, MATCHES_COLLECT)
    print(docs)
    return docs


def update_match(name: str, otherName: str, favorite: bool) -> bool:
    """
    Function to update match (depending on field we want to change)
    """
    if (not users.exists(name)) or (not users.exists(otherName)):
        raise ValueError('Invalid entry')

    dbc.connect_db()
    currUser = dbc.fetch_one(MATCHES_COLLECT, {NAME: name})  # finding person
    if (favorite):
        dbc.update_one(MATCHES_COLLECT, {NAME: name},
                       {"$push": {FAVORITES: otherName}}
                       )
    else:
        if otherName in currUser[FAVORITES]:
            dbc.update_one(MATCHES_COLLECT, {NAME: name},
                           {"$pull": {FAVORITES: otherName}}
                           )
    return True


def unmatch_users(name: str, other_user_name: str):
    """
    Unmatches two users by removing their connection.
    """
    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invlaid entry')

    dbc.connect_db()
    currUser = dbc.fetch_one(MATCHES_COLLECT, {NAME: name})  # finding person
    otherUser = dbc.fetch_one(MATCHES_COLLECT, {NAME: other_user_name})

    try:
        if currUser and (other_user_name in currUser[MATCHES]):
            dbc.update_one(MATCHES_COLLECT, {NAME: name},
                           {"$pull": {MATCHES: other_user_name}}
                           )
            if other_user_name in currUser[FAVORITES]:
                dbc.update_one(MATCHES_COLLECT, {NAME: name},
                               {"$pull": {FAVORITES: other_user_name}}
                               )

        if otherUser and (name in otherUser[MATCHES]):
            dbc.update_one(MATCHES_COLLECT, {NAME: other_user_name},
                           {"$pull": {MATCHES: name}}
                           )
            if name in otherUser[FAVORITES]:
                dbc.update_one(MATCHES_COLLECT, {NAME: other_user_name},
                               {"$pull": {FAVORITES: name}}
                               )

    except ValueError:
        raise ValueError('Users are not unmatched')

    return True


def newMatchUsers(name: str, other_user_name: str) -> bool:

    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invalid entry')

    dbc.connect_db()

    currUser = dbc.fetch_one(MATCHES_COLLECT, {NAME: name})  # finding person
    otherUser = dbc.fetch_one(MATCHES_COLLECT, {NAME: other_user_name})

    if (not currUser) and (not otherUser):
        # TODO: need to add favorite as well
        dbc.insert_one(MATCHES_COLLECT,
                       {NAME: name, MATCHES: [other_user_name], FAVORITES: []})
        dbc.insert_one(MATCHES_COLLECT,
                       {NAME: other_user_name, MATCHES: [name], FAVORITES: []})

    # This is checking for duplicates for each user
    elif currUser and (other_user_name in currUser[MATCHES]):
        # checking FRS for other username
        raise ValueError('Duplicate entry')

    elif otherUser and (name in otherUser[MATCHES]):
        # checking FRS for other username
        raise ValueError('Duplicate entry')

    # if currUser doesn't exist, create it
    # vs. updating other_user since it already exists
    elif not currUser:
        dbc.insert_one(MATCHES_COLLECT,
                       {NAME: name, MATCHES: [other_user_name], FAVORITES: []})
        # Add name to friend_request_received list of other_user_name
        dbc.update_one(MATCHES_COLLECT, {NAME: other_user_name},
                       {"$push": {MATCHES: name}}
                       )

    # if otherUser doesn't exist, create it
    # vs. updating currUser since it already exists
    elif not otherUser:
        dbc.insert_one(MATCHES_COLLECT,
                       {NAME: other_user_name, MATCHES: [name], FAVORITES: []})
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(MATCHES_COLLECT, {NAME: name},
                       {"$push": {MATCHES: other_user_name}}
                       )

    else:  # BOTH EXIST
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(MATCHES_COLLECT, {NAME: name},
                       {"$push": {MATCHES: other_user_name}}
                       )

        # Add name to friend_request_received list of other_user_name
        dbc.update_one(MATCHES_COLLECT, {NAME: other_user_name},
                       {"$push": {MATCHES: name}}
                       )

    return True


# THIS IS FOR FRIEND REQUESTS ***
def fetch_friendReqs() -> dict:
    """
    A function to return all matches in the data store.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, FRIENDREQ_COLLECT)


def deleteFriendReq(name: str, other_user_name: str):
    # name = darecklocal (FRS of cors)
    # othername = cors (FRR of darecklocal)
    # delete name from FRS cors / othernmae
    # delete othername from FRR darecklocal / name
    """
    Retract a sent out Friend Request (or when match successful*)
    """
    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Remove the match for name
    dbc.connect_db()
    currUser = dbc.fetch_one(FRIENDREQ_COLLECT, {NAME: name})  # finding person
    otherUser = dbc.fetch_one(FRIENDREQ_COLLECT, {NAME: other_user_name})

    try:
        if currUser and (other_user_name in currUser[FRR]):
            dbc.update_one(FRIENDREQ_COLLECT, {NAME: name},
                           {"$pull": {FRR: other_user_name}}
                           )

        if otherUser and (name in otherUser[FRS]):
            dbc.update_one(FRIENDREQ_COLLECT, {NAME: other_user_name},
                           {"$pull": {FRS: name}}
                           )

    except ValueError:
        raise ValueError('Users are not unmatched')

    return True


def acceptFriendReq(name: str, otherName: str) -> bool:
    """
    Function to accept friend request
    """
    if (not users.exists(name)) or (not users.exists(otherName)):
        raise ValueError("Match can't be blank")

    # FIRST: accepting a friendReq:
    newMatchUsers(name, otherName)

    # AFTER: a friendReq
    deleteFriendReq(name, otherName)

    return True


""" This will be the new way we store friend
requests for both the sending/recieving user.
We'll be using a FR_SENT list for the sending user,
and corresponding FR_RECIEVED list for the recieving user."""


def newSendFriendReq(name: str, other_user_name: str) -> bool:

    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invalid entry')

    dbc.connect_db()

    # TO DO: need to check for duplicates ***
    currUser = dbc.fetch_one(FRIENDREQ_COLLECT, {NAME: name})  # finding person
    otherUser = dbc.fetch_one(FRIENDREQ_COLLECT, {NAME: other_user_name})

    if (not currUser) and (not otherUser):
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: name, FRS: [other_user_name], FRR: []})
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: other_user_name, FRS: [], FRR: [name]})

    # This is checking for duplicates for each user
    elif currUser and (other_user_name in currUser[FRS]):
        # checking FRS for other username
        raise ValueError('Duplicate entry')

    elif otherUser and (name in otherUser[FRR]):
        # checking FRS for other username
        raise ValueError('Duplicate entry')

    # if currUser doesn't exist, create it
    # vs. updating other_user since it already exists
    elif not currUser:
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: name, FRS: [other_user_name], FRR: []})
        # Add name to friend_request_received list of other_user_name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: other_user_name},
                       {"$push": {FRR: name}}
                       )

    # if otherUser doesn't exist, create it
    # vs. updating currUser since it already exists
    elif not otherUser:
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: other_user_name, FRS: [], FRR: [name]})
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: name},
                       {"$push": {FRS: other_user_name}}
                       )

    else:  # BOTH EXIST
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: name},
                       {"$push": {FRS: other_user_name}}
                       )

        # Add name to friend_request_received list of other_user_name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: other_user_name},
                       {"$push": {FRR: name}}
                       )

    return True
