#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
FLASK_APP=$PWD/bookMarkLibrary/run.py flask db upgrade

#if [ ! -z "$STORAGE_PATH" ] ; \
#  then gcsfuse -o allow_other $STORAGE_PATH /app/bookMarkLibrary/storage ; \
  fi
#if [ ! -z "$LOG_PATH" ] ; \
#  then gcsfuse -o allow_other $LOG_PATH /app/log ; \
#  fi