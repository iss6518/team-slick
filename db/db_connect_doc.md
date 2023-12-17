HOW TO USE MONGODB ON CLOUD:
1. under the team-slick directory need to set MONGODB_PASSWORD environment variable
(export MONGODB_PASSWORD='sweProjectIccha')
2. need to also set the CLOUD_MONGO environment variable to 1 so that CLOUD is used and not local
(export CLOUD_MONGO=1)
3. now run ./local.sh to start swagger
4. use the /users endpoint to retrieve a list of all users in the commongroundDB cloud database
5. use the POST /users endpoint to add a new user

*** if the CLOUD_MONGO environment variable is not set to one the DB connection will default to the local DB ***
