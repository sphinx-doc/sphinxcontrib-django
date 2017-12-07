import sphinxcontrib_django.docstrings

__version__ = "0.1"


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


#: Example Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.6', None),
    'django': ('https://docs.djangoproject.com/en/stable/', 'https://docs.djangoproject.com/en/stable/_objects/'),
    'braces': ('https://django-braces.readthedocs.org/en/latest/', None),
    'select2': ('https://django-select2.readthedocs.org/en/latest/', None),
    'celery': ('https://celery.readthedocs.org/en/latest/', None),
}
