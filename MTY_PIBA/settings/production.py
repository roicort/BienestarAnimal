from .base import *

DEBUG = True

SECRET_KEY = "django!q*mt*uab7p=rmo4zpk%uz9*o7ux#ayp+%&x)fp6kq(734lp^m"

ALLOWED_HOSTS = [
    "bienestaranimal.drf.apismty.gob.mx",
    "https://bienestaranimal.drf.apismty.gob.mx",
    ]

CORS_ALLOWED_ORIGINS = [
    "mascotasmonterrey.web.app",
    "https://mascotasmonterrey.web.app",
    ]

CSRF_TRUSTED_ORIGINS = [
    "bienestaranimal.drf.apismty.gob.mx",
    "https://bienestaranimal.drf.apismty.gob.mx",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SPECTACULAR_SETTINGS = {
    'TITLE': 'PIBA API',
    'DESCRIPTION': 'Plafaforma de Bienestar Animal de Monterrey',
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
