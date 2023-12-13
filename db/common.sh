#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=commongroundDB
USER=iccha02
CONNECT_STR="mongodb+srv://atlascluster.xd0fj6a.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/icchasingh/softwareEngClass/team-slick/db
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGODB_PASS ]
then
    echo "You must set MONGODB_PASSWORD in your env before running this script."
    exit 1
fi 

declare -a MatchesCollections=("matches" "users")
