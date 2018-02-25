"""
Django settings for wharf project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY", ')u-_udqved=rq9p3fc-6mv6xh7y%slo-5d=h1590(k19e+srxt')

DEBUG = 'DYNO' not in os.environ # Debug off when deployed

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jinja',
    'bootstrapform_jinja',
    'django_celery_results',
    'apps'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wharf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "match_extension": None,
            "app_dirname": "templates",
        },
    },
]

if "CACHE_URL" in os.environ:
    cache_url = os.environ["CACHE_URL"]
elif "REDIS_URL" in os.environ:
    cache_url = "%s/1" % os.environ["REDIS_URL"]
else:
    raise Exception("Neither CACHE_URL nor REDIS_URL set in environment")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": cache_url,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

WSGI_APPLICATION = 'wharf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')) }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# Wharf settings

DOKKU_HOST = os.environ.get("DOKKU_SSH_HOST", "127.0.0.1")
DOKKU_SSH_PORT = int(os.environ.get("DOKKU_SSH_PORT", "22"))

# Celery settings

if "BROKER_URL" in os.environ:
    broker_url = os.environ["BROKER_URL"]
elif "REDIS_URL" in os.environ:
    broker_url = "%s/0" % os.environ["REDIS_URL"]
else:
    raise Exception("Neither BROKER_URL nor REDIS_URL set in environment")

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = broker_url
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SERIALISER = "pickle" # To fix exception serialisation. See https://github.com/celery/celery/pull/3592