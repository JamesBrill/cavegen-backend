"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from datetime import timedelta
import backend.utils

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(j*)!8fxw_f1h&l5p&bgqzxg4_-)s5_o#3f=36j_%b9o@&8j_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('CAVEGEN_ENV', None) == 'development'

ALLOWED_HOSTS = [
    '192.168.31.12',
    '.elasticbeanstalk.com',
    '.cavegen.com'
]

CORS_ORIGIN_WHITELIST = (
    'cavegen.com',
    'droidfreak36.com',
    'localhost:3000'
)

# Application definition

INSTALLED_APPS = [
    'authentication.apps.AuthenticationConfig',
    'caves.apps.CavesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {}

if 'RDS_DB_NAME' in os.environ:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT']
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cavegen',
        'USER': 'cavegen',
        'PASSWORD': 'vIw3G5ROoqurfWV2ZiwRbZuF',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URLS
if os.environ.get('CAVEGEN_ENV', None) == 'development':
    _BASE = 'http://localhost:3000/'
else:
    _BASE = 'http://cavegen.com/'

EXTERNAL_URLS = {
    'BASE': _BASE,
    'BASE_WITH_TOKEN': _BASE + 'login?token={id_token}',
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ]
}

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'backend.utils.username_handler',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_EXPIRATION_DELTA': timedelta(hours=24)
}

if 'JWT_SECRET_KEY' in os.environ and 'JWT_AUDIENCE' in os.environ:
    secret_key = os.environ['JWT_SECRET_KEY']
    JWT_AUTH['JWT_SECRET_KEY'] = secret_key
    JWT_AUTH['JWT_ENCODED_SECRET_KEY'] = secret_key
    JWT_AUTH['JWT_AUDIENCE'] = os.environ['JWT_AUDIENCE']
