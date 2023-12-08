#!/bin/sh
# Script to backup production db to JSON files 

. ./common.sh

for collection in ${MatchesCollections[@]}; do 
    echo "Restoring $collection"
    $IMP --db=$DB --collection $collection --drop --file $BKUP_DIR/$collection.json
done