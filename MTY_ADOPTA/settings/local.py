from .base import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ADOPTAMTY',
        'USER': 'postgres',
        'HOST': '127.0.0.1',
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ADOPTA API',
    'DESCRIPTION': 'Adoptamonterrey',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "https://adopta.monterrey.gob.mx",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
    r"^http://localhost:9000$",
    r"^http://127.0.0.1:9000$",
    r"^http://127.0.0.1:8000$",
]