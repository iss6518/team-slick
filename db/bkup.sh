#!/bin/bash
# Script to backup production db to JSON files.


. ./common.sh

for collection in ${MatchesCollections[@]}; do 
    echo "Backing up $collection"
    $EXP --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json $CONNECT_STR --username $USER --password $MONGODB_PASS
done

git add $BKUP_DIR/*.jsonc
git add $BKUP_DIR/*.json
git commit $BKUP_DIR/*.json -m "Mongo DB backup"
git pull origin master
git push origin master