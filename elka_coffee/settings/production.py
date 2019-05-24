from elka_coffee.settings.settings import *

ALLOWED_HOSTS = ['elka-coffee.herokuapp.com']

DEBUG = False

DATABASES['default'] = dj_database_url.config(default='postgres://fulpwaggtrzyzw:73210d861d1d572df5217ba67ddc686759e1f5e1cecca1ee06cfa7ce28992bf0@ec2-54-83-36-37.compute-1.amazonaws.com:5432/dftcuad261nv42')
