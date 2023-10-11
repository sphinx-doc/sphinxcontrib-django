"""
Dummy Django settings file
"""
from __future__ import annotations

SECRET_KEY = "dummy-key"

#: These are the installed apps
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "dummy_django_app",
]

USE_TZ = False
