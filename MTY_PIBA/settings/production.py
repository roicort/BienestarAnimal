from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-!q*mt*uab7p=rmo4zpk%uz9*o7ux#ayp+%&x)fp6kq(734lp^m"

ALLOWED_HOSTS = [
    "adopta.drf.dev.mun.apismty.gob.mx"
    ]

CORS_ALLOWED_ORIGINS = [
    "https://adoptamos.web.app",
    "adoptamos.web.app",
    ]

CSRF_TRUSTED_ORIGINS = [
    "https://adopta.drf.dev.mun.apismty.gob.mx",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SPECTACULAR_SETTINGS = {
    'TITLE': 'BTS API',
    'DESCRIPTION': 'Bolsa de Empleo de Monterrey',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass