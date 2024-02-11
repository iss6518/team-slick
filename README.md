# flask-api
An example flask rest API server.

To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.

Access goals here [ProgressAndGoals](./ProgressAndGoals.md)

# Instructions to run back-end for front-end development
## Running the back-end:

The back-end must be running in the background in order to link to
the front-end. 

If you haven't done so, open a new terminal window and clone the team-slick BE repo using the script:

### `git clone https://github.com/iss6518/team-slick.git`

cd into your team-slick directory and run all necessary set up commands:

1) to set your python environment variable
### export PYTHONPATH=$PYTHONPATH:$(pwd)

2) to pip install necessary dependancies for project
### make dev_env

3) to start a mongo service on your device
### sudo service mongod start

4) to signin to our cloud mongoDB 
### export MONGODB_PASSWORD='INSERT THE MONGODB PW HERE'

5) set to 1 in order to run against our cloud mongoDB
### export CLOUD_MONGO=1

6) to run the swagger endpoint on http://127.0.0.1:8000/
### ./local.sh

