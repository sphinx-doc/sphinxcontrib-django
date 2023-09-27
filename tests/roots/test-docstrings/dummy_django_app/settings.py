"""
Dummy Django settings file
"""
from __future__ import annotations

SECRET_KEY = "dummy-key"

ROOT_URLCONF = "dummy_django_app.urls"

#: These are the installed apps
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "dummy_django_app",
    "dummy_django_app2",
]

USE_TZ = False
