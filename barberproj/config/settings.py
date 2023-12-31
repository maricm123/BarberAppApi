from datetime import timedelta
from distutils.util import strtobool
import os
from pathlib import Path
from dotenv import load_dotenv
import django_heroku
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


load_dotenv()  # take environment variables from .env.

ALLOWED_HOSTS = []

SECRET_KEY = os.environ["DJ_SECRET_KEY"]

DEBUG = bool(strtobool(os.environ["DJ_DEBUG"]))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_heroku',
    'barberProfile.apps.BarberprofileConfig',
    'schedule.apps.ScheduleConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'

# Activate Django-Heroku.
django_heroku.settings(locals())

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# Database configuration for local environment (override Heroku conf because of SSL troubles)
USE_HEROKU_DB_CONF = bool(strtobool(os.environ["DJ_USE_HEROKU_DB_CONF"]))
if not USE_HEROKU_DB_CONF:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'barber',
            'USER': 'postgres',
            'PASSWORD': 'admin',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     # globalno setovana permisija
#     # 'DEFAULT_PERMISSION_CLASSES': [
#     #     'rest_framework.permissions.IsAuthenticated',
#     # ]
# }

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}


#  ----------------- SIMPLE JWT SETTINGS ---------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    # "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.MyTokenObtainPairSerializer",
    # 'BLACKLIST_AFTER_ROTATION': True,
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    # 'ROTATE_REFRESH_TOKENS': False,
    # "Bearer <Token>",
}


ALLOWED_HOSTS=['*']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]

AUTH_USER_MODEL = "barberProfile.User"


# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


####################################################################################################
# Mailjet (mailing)
####################################################################################################

EMAIL_BACKEND = os.environ["DJ_EMAIL_BACKEND"]  # Console for local env, Dummy for staging, etc.
EMAIL_HOST = os.environ.get("DJ_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("DJ_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("DJ_EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("DJ_EMAIL_PORT")
EMAIL_USE_TLS = bool(strtobool(os.environ["DJ_EMAIL_USE_TLS"]))