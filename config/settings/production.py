"""Configuring Django Mutadi app for Heroku"""
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.environ["DJANGO_DEBUG"]

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_SSL_REDIRECT = True

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# Activate Django-Heroku.
django_heroku.settings(locals())
