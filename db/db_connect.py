import os

import pymongo as pm

# import certifi

# import ssl

# ca = certifi.where()

LOCAL = "0"
CLOUD = "1"

COMMONGROUND_DB = 'commongroundDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... (might have to rethink this)
    Also set global client variable.
    We should either return a client OR set a client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGODB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://iccha02:{password}'
                                    + '@atlascluster.xd0fj6a.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # atlascluster.xd0fj6a.mongodb.net
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=COMMONGROUND_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def update_one(collection, filter, doc, db=COMMONGROUND_DB):
    """
    Update a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].update_one(filter, doc)


def fetch_one(collection, filt, db=COMMONGROUND_DB):
    # Find with a filter and return on the first doc found.

    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=COMMONGROUND_DB):
    # Find with a filter and return on the first doc found.

    client[db][collection].delete_one(filt)


def fetch_all(collection, db=COMMONGROUND_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=COMMONGROUND_DB):
    ret = {}
    for doc in client[db][collection].find():
        print(doc)
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
