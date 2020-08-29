"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
import mimetypes
import datetime
import django_heroku
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aywdcgi@!l0$y!rfgcv6eutfc=7v6e1)a*iamctkej^zrs067o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '.vfs.cloud9.us-east-1.amazonaws.com',
    '127.0.0.1','api.ideeza.com',
    'sensoi-api.herokuapp.com'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django_middleware_global_request',
    'whitenoise',
    'corsheaders',
    'store',
    'user',
    'product',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_USER_MODEL = 'user.User'

ROOT_URLCONF = 'sensai.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'sensai.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

"""
Host
ec2-52-204-232-46.compute-1.amazonaws.com
Database
datpssmjs67r2c
User
czvppfdonajvsm
Port
5432
Password
82ef23dfa47db55093c6c27ea0907045a64b4ef0fa5de9aba11152d62f411b47
URI
postgres://czvppfdonajvsm:82ef23dfa47db55093c6c27ea0907045a64b4ef0fa5de9aba11152d62f411b47@ec2-52-204-232-46.compute-1.amazonaws.com:5432/datpssmjs67r2c
Heroku CLI
heroku pg:psql postgresql-concave-62483 --app sensoi-api


"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'datpssmjs67r2c'),
        'USER': os.environ.get('DB_USER', 'czvppfdonajvsm'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '82ef23dfa47db55093c6c27ea0907045a64b4ef0fa5de9aba11152d62f411b47'),
        'HOST': os.environ.get('DB_HOST', 'ec2-52-204-232-46.compute-1.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'UNICODE_JSON': False
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
     {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
]

ENABLE_USER_REGISTRATION = True

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://localhost:9000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000",
    "https://sensai-ui.herokuapp.com",
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_INFO': 'config.urls.local.openapi_info',
}


JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

mimetypes.add_type("text/css", ".css", True)

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

django_heroku.settings(locals())