import sys

import django

__version__ = "0.4"


def setup(app):
    """Allow this module to be used as sphinx extension.
    This attaches the Sphinx hooks.

    :type app: sphinx.application.Sphinx
    """
    import sphinxcontrib_django.docstrings
    import sphinxcontrib_django.roles

    # Setup both modules at once. They can also be separately imported to
    # use only fragments of this package.
    sphinxcontrib_django.docstrings.setup(app)
    sphinxcontrib_django.roles.setup(app)


#: Example Intersphinx mapping, linking to project versions
python_version = ".".join(map(str, sys.version_info[0:2]))
django_version = ".".join(map(str, django.VERSION[0:2]))
intersphinx_mapping = {
    'python': ('https://docs.python.org/' + python_version, None),
    'django': ('https://docs.djangoproject.com/en/{}/'.format(django_version), 'https://docs.djangoproject.com/en/{}/_objects/'.format(django_version)),
    'braces': ('https://django-braces.readthedocs.org/en/latest/', None),
    'select2': ('https://django-select2.readthedocs.org/en/latest/', None),
    'celery': ('https://celery.readthedocs.org/en/latest/', None),
}
