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
HELLO_EP = '/hello'
INTERFACE_MENU_EP = '/interface_menu'

USERS_EP = '/users'
MATCHES_EP = '/matches'
FRIENDREQ_EP = '/friendRequest'
FRIENDREQACC_EP = '/friendRequestAccept'

INTERFACE_MENU_NM = 'Interface Menu'
USER_ID = 'User ID'
MATCH_ID = 'Match ID'
FRIENDREQ_ID = 'FriendReq ID'

HELLO_RESP = 'hello'
UNMATCH_USERS = 'unmatch'
DELETE = 'delete'

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


user_fields = api.model('NewUser', {
    users.NAME: fields.String,
    users.AGE: fields.Integer,
    users.GENDER: fields.String,
    users.INTERESTS: fields.String
})


match_fields = api.model('matchUser', {
    interface.NAME: fields.String,
    interface.OTHER_USER: fields.String
})


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports various operations on our users, such as
    listing, adding, updating, and deleting users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: users.fetch_users(),
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
        name = request.json[users.NAME]
        age = request.json[users.AGE]
        gender = request.json[users.GENDER]
        interests = request.json[users.INTERESTS]
        try:
            new_id = users.add_user(name, age, gender, interests)
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
        name = request.json[users.NAME]
        age = request.json[users.AGE]
        gender = request.json[users.GENDER]
        interests = request.json[users.INTERESTS]

        newValues = {
                users.AGE: age,
                users.GENDER: gender,
                users.INTERESTS: interests
                }

        try:
            updated_id = users.update_user(name, newValues)
            if updated_id is False:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: updated_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Found')
    def delete(self):
        """
        deletes user by name
        """
        name = request.json[users.NAME]
        try:
            users.del_user(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{MATCHES_EP}')
class Matches(Resource):
    """
    This class allows a user to match or unmatch with another user.
    """

    def get(self):
        """
        This method returns all matches.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Matches',
            DATA: interface.fetch_matches(),
            MENU: INTERFACE_MENU_EP,
            RETURN: INTERFACE_MENU_EP,
        }

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def delete(self):
        """
        Allows a user to unmatch with another user.
        """
        name = request.json[interface.NAME]
        other_user_name = request.json[interface.OTHER_USER]
        try:
            interface.unmatch_users(name, other_user_name)
            return {'Message': 'Users unmatched successfully'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Allows a user to match with another user.
        """
        name = request.json[interface.NAME]
        other_user_name = request.json[interface.OTHER_USER]
        try:
            interface.match_users(name, other_user_name)
            return {'Message': 'Users matched successfully'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self):
        """
        Update a match.
        """
        name = request.json[interface.NAME]
        otherName = request.json[interface.OTHER_USER]

        try:
            updated_id = interface.update_match(name, otherName)
            if updated_id is False:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {MATCH_ID: updated_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# THIS IS FOR FRIEND REQUESTS
@api.route(f'{FRIENDREQ_EP}')
class FriendReqs(Resource):
    """
    This class allows a user to send a friend request to another user.
    The user can accept or decline this.
    """

    def get(self):
        """
        This method returns all friend requests.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current FriendRequests',
            DATA: interface.fetch_friendReqs(),
            MENU: INTERFACE_MENU_EP,
            RETURN: INTERFACE_MENU_EP,
        }

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def delete(self):
        """
        Allows a user to RETRACT a friend request.
        """
        name = request.json[interface.NAME]
        other_user_name = request.json[interface.OTHER_USER]
        try:
            interface.deleteFriendReq(name, other_user_name)
            return {'Message': 'Users friend request retracted successfully'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Allows a user to send a friend request to another user.
        """
        name = request.json[interface.NAME]
        other_user_name = request.json[interface.OTHER_USER]
        try:
            interface.sendFriendRequest(name, other_user_name)
            return {'Message': 'Users sent a friend request successfully'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self):
        """
        Decline a friend request.
        """
        name = request.json[interface.NAME]
        otherName = request.json[interface.OTHER_USER]

        try:
            updated_id = interface.deleteFriendReq(name, otherName)
            # Once user declines, friendReq should be deleted for both users
            if updated_id is False:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {MATCH_ID: updated_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{FRIENDREQACC_EP}')
class FriendReqsAccept(Resource):
    @api.expect(match_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self):
        """
        Accept a friend request.
        """
        name = request.json[interface.NAME]
        otherName = request.json[interface.OTHER_USER]

        try:
            updated_id = interface.acceptFriendReq(name, otherName)
            # Once user accepts, friendReq should be DELETED for both users
            if updated_id is False:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {MATCH_ID: updated_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
