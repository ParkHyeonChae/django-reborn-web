from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inje_reborn_DB',
        'USER': 'inje_reborn',
        'PASSWORD': os.environ.get('POSTGRESQL_PW'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Heroku: Update database configuration from $DATABASE_URL.

import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)