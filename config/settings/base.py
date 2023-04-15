"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bkgddy0+cn=+=^)_fjno@t!4^-2%mnsio-nqu$)*ir_*my9gjk'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'daphne',  # need for channels
    'channels',  # intercepts all

    # local
    'courses',
    # !important
    # If you see the Logged out page of the Django administration site instead of your own Logged out page, check the INSTALLED_APPS setting of your project and make sure that django. contrib.admin comes a#er the  application that provides login and logout templates.
    #
    # Both applications contain logged-out templates located in the same relative path. The Django template loader will go through the diﬀerent applications in the INSTALLED_APPS list and use the ﬁrst template it ﬁnds.

    'students',

    # 3d party
    'embed_video',
    'debug_toolbar',
    'chat',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3d party
    'redisboard',
    # needs to pass its migrations to db after install and in admin panel add redis server redis://localhost:6380/0  where 0 is the database number for redis

    'rest_framework',  # django rest framework

]
# middleware is invoked in the given order during request phase
# and in reverse order during response phase!!!
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # add debug toolbar
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',  # per site cache in the response phase is invoked after the CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # per site cache (needs data from Csrf in the response phase)
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# per site cache middleware will cache all views including the admin dashboard (not good)
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # fifteen minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'  # project prefix in case many projects use the same backend

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'  # replaced by asgi

ASGI_APPLICATION = 'config.asgi.application'  # for the channels 3d party app

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# moved to particular local or prod


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'  # base url for media files
MEDIA_ROOT = BASE_DIR / 'media'  # local path for media files for development

CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
    #     'LOCATION': os.getenv('MEMCACHE_HOST') + ':' + os.getenv('MEMCACHE_PORT'),
    #     # 'TIMEOUT',
    # }
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://' + os.getenv('REDIS_HOST') + ':' + os.getenv('REDIS_PORT'),
    }
}

INTERNAL_IPS = [
    '127.0.0.1',  # django debug toolbar will only display if your ip address matches this entry
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',  # read only access for anonymous users
    ]
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT')),
            ]
        }
    }
}
