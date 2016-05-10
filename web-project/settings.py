import os

_ROOT = os.path.dirname(__file__)

TITLE = ""
SUB_TITLE = ""
DOMAIN_NAME = ""
HANDLERS = (
    'web',
)

LOGIN_URL = "/login"
COOKIE_SECRET = "/hncZPV7TVaxY/krcQFc9Ujm6blLPk9Bsh6xdIYfAuc="

MYSQL_HOST = ''
MYSQL_DATABASE_NAME = ''
MYSQL_USER_NAME = ''
MYSQL_PASS_WORD = ''

MONGO_HOST = ''
MONGO_PORT = 27017
MONGO_USER = ''
MONGO_PASSWD = ''

REDIS_ADDRESS = ''
REDIS_PORT = '6379'
REDIS_PASSWD = ''
REDIS_INDEX = 1

WEBMASTER = ''
ADMIN_EMAILS = []


OAUTH_SETTINGS = {
    'client_id': '',
    'client_secret': '',
    'base_url': '',
    'redirect_url': ''
}

try:
    from local_settings import *
except ImportError:
    pass
