"""
Django settings for MTY_ADOPTA project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from google.oauth2 import service_account
from dotenv import load_dotenv

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "modelcluster",
    "taggit",
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'django.contrib.gis',
    'rest_framework',
    'corsheaders',
    'storages',
    'mty_firebase_auth',
    'django_filters',
    'drf_dynamic_fields',
    'drf_spectacular',
    'auditlog',

    'apirest',
    'users',
    'base',
    'asociaciones',
    'perfiles',
    'animales',
    'import_export',
    'daterange.apps.DateRangeFilterConfig',
    'gisserver',
    #'wms',

]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "mty_firebase_auth.middleware.FirebaseEmailPasswordAuthMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "threadlocals.middleware.ThreadLocalMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "MTY_ADOPTA.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "MTY_ADOPTA.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash

AUTH_USER_MODEL = 'users.User'

MTY_FIREBASE_AUTH = {
    'FIREBASE_SERVICE_ACCOUNT_KEY': os.path.abspath(os.path.join(BASE_DIR, '_gcp_sa', 'firebase_auth_service_account_key.json')),
    'FIREBASE_APP_CONFIG_KEY': os.path.abspath(os.path.join(BASE_DIR, '_gcp_sa', 'firebase_auth_app_config.json')),
    'FIREBASE_CREATE_LOCAL_USER': True,
    'FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME': False,
    'FIREBASE_AUTH_HEADER_PREFIX': 'Bearer'
}

os.environ['FIREBASE_SERVICE_ACCOUNT_KEY'] = str(
    MTY_FIREBASE_AUTH['FIREBASE_SERVICE_ACCOUNT_KEY'])
os.environ['FIREBASE_APP_CONFIG_KEY'] = str(
    MTY_FIREBASE_AUTH['FIREBASE_APP_CONFIG_KEY'])
os.environ['FIREBASE_CREATE_LOCAL_USER'] = str(
    MTY_FIREBASE_AUTH['FIREBASE_CREATE_LOCAL_USER'])
os.environ['FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME'] = str(
    MTY_FIREBASE_AUTH['FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME'])
os.environ['FIREBASE_AUTH_HEADER_PREFIX'] = str(
    MTY_FIREBASE_AUTH['FIREBASE_AUTH_HEADER_PREFIX'])

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/minute',
        'user': '1000/minute',
        'loginAttempts': '3/hr',
    },
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'mty_firebase_auth.authentication.FirebaseAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

for env_file in ('env', '.env'):
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'