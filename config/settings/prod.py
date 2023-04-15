import os

from .base import *
load_dotenv('.env.prod')


DEBUG = False
# DEBUG = True

# when view raises an exception, log will be sent to emails listed in ADMINS via email
ADMINS = [
    ('admin', 'contact@vadzimk.com'),
]

# hosts that are allowed to serve this project
ALLOWED_HOSTS = ['*'] # ip address of the website or localhost

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# update CACHES and CHANNEL_LAYERS is not necessary bc they were specified in env


