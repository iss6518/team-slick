"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus
import werkzeug.exceptions as wz

from flask import Flask, request
from flask_restx import Resource, Api, fields
import db.users as users
import db.interface as interface

# creating flash application
app = Flask(__name__)
api = Api(app)
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Text Game!"

# forming some endpoint URLs
DELETE = 'delete'
USERS_EP = '/users'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'

INTERFACE_EP = '/interfaces'
INTERFACE_MENU_EP = '/interface_menu'
INTERFACE_MENU_NM = 'Interface Menu'
USER_ID = 'User ID'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
UNMATCH_EP = f'{USERS_EP}/unmatch'

TYPE = 'Type'
DATA = 'Data'
MENU = 'Menu'
TITLE = 'Title'
RETURN = 'Return'


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


# need to add an (maybe external) endpoint for login (ex: signin with google)


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


@api.route(f'{DEL_USER_EP}/<name>')
class DelUser(Resource):
    """
    Deletes a user by name
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name):
        """
        deletes user by name
        """
        try:
            interface.del_user(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NOT_FOUND(f'{str(e)}')


user_fields = api.model('NewUser', {
    interface.NAME: fields.String,
    interface.AGE: fields.Integer,
    interface.GENDER: fields.String,
    interface.INTERESTS: fields.String
})


@api.route(f'{INTERFACE_EP}')
class Interface(Resource):
    """
    This class supports various operations on our interface, such as
    listing users, and adding a user.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: interface.fetch_users(),
            MENU: INTERFACE_MENU_EP,
            RETURN: INTERFACE_MENU_EP,
        }

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        name = request.json[interface.NAME]
        age = request.json[interface.AGE]
        gender = request.json[interface.GENDER]
        interests = request.json[interface.INTERESTS]
        try:
            new_id = interface.add_user(name, age, gender, interests)
            if new_id is False:  # add_user return true if _id is None
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self):
        """
        Update a user.
        """
        name = request.json[interface.NAME]
        age = request.json[interface.AGE]
        gender = request.json[interface.GENDER]
        interests = request.json[interface.INTERESTS]

        newValues = {
                interface.AGE: age,
                interface.GENDER: gender,
                interface.INTERESTS: interests
                }

        try:
            updated_id = interface.update_user(name, newValues)
            if updated_id is False:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: updated_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{UNMATCH_EP}/<user_id>/<other_user_id>')
class Unmatch(Resource):
    """
    This class allows a user to unmatch with another user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, user_id, other_user_id):
        """
        Allows a user to unmatch with another user.
        """
        try:
            interface.unmatch_users(user_id, other_user_id)
            return {'Message': 'Users unmatched successfully'}
        except ValueError as e:
            raise wz.NOT_FOUND(f'{str(e)}')