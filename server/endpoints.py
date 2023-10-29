"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
import db.users as users

# creating flash application
app = Flask(__name__)
api = Api(app)
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Text Game!"

# forming some endpoint URLs
USERS_EP = '/users'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
DATA = 'Data'


# creating an endpoint for /hello URL
@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


# creating an endpoint for /endpoint URL
@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


# creating an endpoint for /MainMenu
@api.route(f'/{MAIN_MENU}')
@api.route('/')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Games'},
                    '3': {'url': f'{USERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


# need to add an endpoint (maybe external) for login (ex: signin with email or google)


# endpoint for getting list of friend requests
@api.route(f'{USERS_EP}')
class friendRequests(Resource):
    """
    This class supports fetching a list of friend requests
    """
    def get(self):
        """
        This method returns all friend requests
        """
        return {DATA: users.get_friend_requests()}


# creating an endpoint for /users
@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all pets.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {DATA: users.fetch_users()}
