"""
Dummy Django settings file
"""

SECRET_KEY = "dummy-key"

#: These are the installed apps
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "dummy_django_app",
    "dummy_django_app2",
]

USE_TZ = False
