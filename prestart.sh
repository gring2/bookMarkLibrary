#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
FLASK_APP=$PWD/bookMarkLibrary/run.py flask db upgrade