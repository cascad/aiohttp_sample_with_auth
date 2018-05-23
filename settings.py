from os.path import isfile

from envparse import env

if isfile('environments.env'):
    env.read_envfile('environments.env')

DEBUG = env.bool('DEBUG', default=True)

SITE_HOST = env.str('HOST')
SITE_PORT = env.int('PORT')
MASTER_KEY = env.str('MASTER_KEY')
COOKIE_SECRET = env.str('COOKIE_SECRET')
STATIC_PATH = env.str('STATIC_PATH')
STATIC_URL = env.str('STATIC_URL')
TEMPLATE_PATH = env.str('TEMPLATE_PATH')

SESSION_EXPIRE = 3600 * 24 * 15  # 3600 * 24 * 30
HASH_EXPIRE = 3600 * 2  # 3600 * 24 * 30
COOKIE_EXPIRE = 3600 * 24

PROJECT_PREFIX = "ldoe_support"

USERS = {
    "admin": {"pwd": "123", "uid": "123"},
    "user": {"pwd": "1  ", "uid": "1"}
}
