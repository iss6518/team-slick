The endpoints file defines and manages the API endpoints for our Flash application (our game). We first define constants linked to a URL and then create the endpoints for the URLs. 

The endpoint definitions handle what a call to the URLs returns to the user. In the case of /hello, the user simply gets a "hello world" back, but we can also configure endpoints that fetch/return information.

For instance, the endpoint for /users fetches all of the users (pets) and the endpoint for /MainMenu will allow the user to interact with menu options. 

Keeping all of the endpoint configurations in one file makes it much easier to test the routing/behavior of an application without having to make changes to the logic behind the main application code. 