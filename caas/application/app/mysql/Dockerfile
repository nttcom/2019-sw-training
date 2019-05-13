FROM mysql:5.7

# prepare initialize data
COPY ./prepare.sql /docker-entrypoint-initdb.d/prepare.sql

# set environment variable
ENV MYSQL_ROOT_PASSWORD password