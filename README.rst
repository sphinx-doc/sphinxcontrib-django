.. image:: https://github.com/timoludwig/sphinxcontrib-django2/workflows/Tests/badge.svg
    :alt: GitHub Workflow Status
    :target: https://github.com/timoludwig/sphinxcontrib-django2/actions?query=workflow%3ATests
.. image:: https://img.shields.io/pypi/v/sphinxcontrib-django2.svg
    :alt: PyPi
    :target: https://pypi.python.org/pypi/sphinxcontrib-django2/
.. image:: https://codecov.io/gh/timoludwig/sphinxcontrib-django2/branch/develop/graph/badge.svg
    :alt: Code coverage
    :target: https://codecov.io/gh/timoludwig/sphinxcontrib-django2
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Black Code Style
    :target: https://github.com/psf/black
.. image:: https://img.shields.io/github/license/timoludwig/sphinxcontrib-django2
    :alt: GitHub license
    :target: https://github.com/timoludwig/sphinxcontrib-django2/blob/develop/LICENSE

sphinxcontrib-django2
=====================

Improvements for the output of Sphinx's autodoc for Django classes.

This is a fork of `sphinxcontrib-django`_, which seems to be no longer maintained.
In comparison to the upstream repository, this provides the following:

* Support for current versions of Python and Django
* Support for ModelForms
* Support Intersphinx mappings to Django classes
* 100% test coverage

The original repository already implemented the following features:

* Properly show which fields a model has.
* Properly show which fields a form has.
* Document the model fields as parameters in the model ``__init__()``.
* Link foreign key and related fields to the documentation of the referenced class.
* Hide irrelevant runtime information like ``declared_fieldsets``, ``fieldsets`` and ``Meta`` from classes.
* A ``:django:setting:`` role to allow linking to Django documentation. (e.g. *:django:setting:`SITE_ID`*)

.. _sphinxcontrib-django: https://github.com/edoburu/sphinxcontrib-django

Installation
------------

Usage:

.. code-block:: bash

    pip install sphinxcontrib-django2

Add to the Sphinx config file (``conf.py``):

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        'sphinxcontrib_django2',
    ]

Autodoc works by importing your code on the fly, and extracting the data from
the Python classes. Thus, the project should be able to import Django models.
Typically the following needs to be added to ``conf.py``:

.. code-block:: python

    sys.path.insert(0, os.path.abspath('../src'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'
    django.setup()

To support the ``:django:setting:`` role, configure Intersphinx:

.. code-block:: python

    intersphinx_mapping = {
        'http://docs.python.org/': None,
        'https://docs.djangoproject.com/en/stable': 'https://docs.djangoproject.com/en/stable/_objects',
    }


Contributing
------------

Pull requests are always welcome!

You can install all requirements of the development setup with `Pipenv`_:

.. code-block:: bash

    pipenv install --dev
    pipenv run pre-commit install

Then, run the tests with:

.. code-block:: bash

    pipenv run coverage run runtests.py

.. _Pipenv: https://pipenv.pypa.io/
