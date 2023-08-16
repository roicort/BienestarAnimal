from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-!q*mt*uab7p=rmo4zpk%uz9*o7ux#ayp+%&x)fp6kq(734lp^m"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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
