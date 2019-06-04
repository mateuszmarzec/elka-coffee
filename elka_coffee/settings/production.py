import dj_database_url

from elka_coffee.settings.settings import *

ALLOWED_HOSTS = ['elka-coffee.herokuapp.com']

DEBUG = True

DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))
