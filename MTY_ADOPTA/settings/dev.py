from .base import *
from dotenv import load_dotenv

env_path = os.path.join(BASE_DIR, 'env')
load_dotenv(env_path)

DEBUG = True

SECRET_KEY = "django-insecure-!q*mt*uab7p=rmo4zpk%uz9*o7ux#ayp+%&x)fp6kq(734lp^m"

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",
    "172.21.50.125"
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SPECTACULAR_SETTINGS = {
    'TITLE': 'BTS API (DEV)',
    'DESCRIPTION': 'Bolsa de Empleo de Monterrey (DEV)',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}

STORAGES = {
    "default": {
        "BACKEND": 'django.core.files.storage.FileSystemStorage'
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

INSTALLED_APPS += ['whitenoise.runserver_nostatic']

try:
    from .local import *
except ImportError:
    pass
