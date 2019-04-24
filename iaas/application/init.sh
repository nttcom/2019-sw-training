#!/bin/bash

DB_DIR=$(cd $(dirname $0) && pwd)
cd $DB_DIR

mysql -u root -p'password' -h 127.0.0.1 -D tododb < init.sql
