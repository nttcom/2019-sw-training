#!/bin/bash

DB_DIR=$(cd $(dirname $0) && pwd)
cd $DB_DIR

mysql -u user -p'password' -h 127.0.0.1 -D tododb < init.sql
