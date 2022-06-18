import os
SECRET_KEY = os.urandom(24)
DEBUG = True

DB_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/cms?charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'abcdefg'