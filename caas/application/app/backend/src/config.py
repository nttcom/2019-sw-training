import os

# get MySQL IP(Environment variable)
MYSQL_IP = os.getenv("MYSQL_IP", "0.0.0.0")

# config has to be implicit in config file. db password has also to be encoded.
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@' + MYSQL_IP + '/tododb?charset=utf8'

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
