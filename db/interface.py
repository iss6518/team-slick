# interface for matching and sending friend requests for our users
import db.db_connect as dbc
import db.users as users
# import db.friend_request_received as friend_rr
# import db.friend_request_sent as friend_rs

USERS_COLLECT = "users"
MATCHES_COLLECT = "matches"
FRIENDREQ_COLLECT = "friendRequests"
# defined as lists
FRIENDREQ_SENT = []
FRIENDREQ_RECIEVED = []

BIG_NUM = 100000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

ID = '_id'
NAME = 'user_name'
OTHER_USER = 'other_user'
FAVORITE = 'favorite'

# added these for fetch_one
# for friend requests
FRR = 'friend_request_received'
FRS = 'friend_request_sent'


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


def update_match(name: str, otherName: str) -> bool:
    """
    Function to update match (depending on field we want to change)
    """
    if not name:  # TODO should use match_exits func ***
        raise ValueError("Match can't be blank")

    filter = {NAME: name, OTHER_USER: otherName}
    thisMatch = dbc.fetch_one(MATCHES_COLLECT, filter)
    setValues = {"$set": {FAVORITE: not (thisMatch[FAVORITE])}}

    dbc.connect_db()
    _id = dbc.update_one(MATCHES_COLLECT, filter, setValues)
    return _id is not None


def unmatch_users(name: str, other_user_name: str):
    """
    Unmatches two users by removing their connection.
    """
    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Remove the match for name
    dbc.connect_db()
    try:
        dbc.del_one(MATCHES_COLLECT, {NAME: name, OTHER_USER: other_user_name})
        dbc.del_one(MATCHES_COLLECT, {NAME: other_user_name, OTHER_USER: name})
    except ValueError:
        raise ValueError('Users are not unmatched')


def match_users(name: str, other_user_name: str) -> bool:
    """
    Match two users by adding their connection.
    """
    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Add the match for name
    dbc.connect_db()
    MATCHA = {NAME: name, OTHER_USER: other_user_name, FAVORITE: False}
    MATCHB = {NAME: other_user_name, OTHER_USER: name, FAVORITE: False}

    _id1 = dbc.insert_one(MATCHES_COLLECT, MATCHA)
    _id2 = dbc.insert_one(MATCHES_COLLECT, MATCHB)
    return _id1 is not None and _id2 is not None


# THIS IS FOR FRIEND REQUESTS ***
def fetch_friendReqs() -> dict:
    """
    A function to return all matches in the data store.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, FRIENDREQ_COLLECT)


def acceptFriendReq(name: str, otherName: str) -> bool:
    """
    Function to accept friend request
    """
    if not name:  # TODO should use match_exits func ***
        raise ValueError("Match can't be blank")

    # filterOne = {NAME: name, OTHER_USER: otherName}
    # filterTwo = {NAME: otherName, OTHER_USER: name}

    # FIRST: accepting a friendReq:
    match_users(name, otherName)

    # AFTER: a friendReq
    returnVal = deleteFriendReq(name, otherName)

    # thisMatch = dbc.fetch_one(MATCHES_COLLECT, filter)
    # setValues = {"$set": {FAVORITE: not (this[FAVORITE])}}

    # dbc.connect_db()
    # _id = dbc.update_one(FRIENDREQ_COLLECT, filter, setValues)
    return returnVal


def deleteFriendReq(name: str, other_user_name: str):
    """
    Retract a sent out Friend Request (or when match successful*)
    """
    if (not users.exists(name)) or (not users.exists(other_user_name)):
        raise ValueError('Invlaid entry')

    # Remove the match for name
    dbc.connect_db()
    try:
        firstDel = {NAME: name, OTHER_USER: other_user_name}
        secondDel = {NAME: other_user_name, OTHER_USER: name}
        dbc.del_one(FRIENDREQ_COLLECT, firstDel)
        dbc.del_one(FRIENDREQ_COLLECT, secondDel)
    except ValueError:
        raise ValueError('Users are not unmatched')

# OLD sendFriendReq that's now been replaced by newSendFriendReq

# def sendFriendReq(name: str, other_user_name: str) -> bool:
#     """
#     Original way to send a friend request to another user.
#     Will be replaced with func below.
#     """
#     if (not users.exists(name)) or (not users.exists(other_user_name)):
#         raise ValueError('Invlaid entry')

#     # Add the match for name
#     dbc.connect_db()
#     FRIENDREQA = {NAME: name, OTHER_USER: other_user_name}
#     FRIENDREQB = {NAME: other_user_name, OTHER_USER: name}

#     _id1 = dbc.insert_one(FRIENDREQ_COLLECT, FRIENDREQA)
#     _id2 = dbc.insert_one(FRIENDREQ_COLLECT, FRIENDREQB)
#     return _id1 is not None and _id2 is not None


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

    # TO DO: Use another function other than .find() ***
    # and solve for why cors saved as an object {} ***

    # elif currUser and currUser[FRS].find(other_user_name):
    #     # checking FRS for other username
    #     raise ValueError('Duplicate entry')

    # elif otherUser and otherUser[FRR].find(name):
    #     # checking FRS for other username
    #     raise ValueError('Duplicate entry')

    elif not currUser:
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: name, FRS: [other_user_name], FRR: []})
        # Add name to friend_request_received list of other_user_name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: other_user_name},
                       {"$push": {"friend_request_received": {NAME: name}}}
                       )

    elif not otherUser:
        dbc.insert_one(FRIENDREQ_COLLECT,
                       {NAME: other_user_name, FRS: [], FRR: [name]})
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: name},
                       {"$push": {"friend_request_sent":
                        {NAME: other_user_name}}}
                       )

    else:
        # Add other_user_name to friend_request_sent list of name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: name},
                       {"$push": {"friend_request_sent":
                        {NAME: other_user_name}}}
                       )

        # Add name to friend_request_received list of other_user_name
        dbc.update_one(FRIENDREQ_COLLECT, {NAME: other_user_name},
                       {"$push": {"friend_request_received": {NAME: name}}}
                       )

    return True
