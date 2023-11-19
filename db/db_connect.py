import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

COMMONGROUND_DB = 'commonGroundDB'

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
            password = os.environ.get("COMMONGROUND_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://gcallah:{password}'
                                    + '@cluster0.eqxbbqd.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
