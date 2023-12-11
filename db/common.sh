#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=commongroundDB
USER=iccha02
CONNECT_STR="mongodb+srv://koukoumongo1.yuf9b.mongodb.net/"
if [ -z $DATA_DIR ]
then 
    DATA_DIR=~/team-slick/db
fi 
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGODB_PASSWORD in your env before running this script."
    exit 1
fi 

declare -a MatchesCollections=("matches" "users")
