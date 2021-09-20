#!/bin/bash

execution="\e[0;36m[INFO]\e[0m"

echo "$execution [STARTING TESTS]"

#START SERVER
. ./run_server.sh

echo "$execution [SERVER-BOOT-COMPLETE]"
#Find tests
sleep 10s

python3 -m unittest tests/test_db.py
python3 -m unittest tests/test_main.py

echo "$execution [STOPPING AND CLEANING UP]"