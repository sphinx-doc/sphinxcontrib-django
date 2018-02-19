.. image:: https://img.shields.io/travis/edoburu/sphinxcontrib-django/master.svg?branch=master
    :target: http://travis-ci.org/edoburu/sphinxcontrib-django
.. image:: https://img.shields.io/pypi/v/sphinxcontrib-django.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-django/
.. image:: https://img.shields.io/pypi/l/sphinxcontrib-django.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-django/
.. image:: https://img.shields.io/codecov/c/github/edoburu/sphinxcontrib-django/master.svg
    :target: https://codecov.io/github/edoburu/sphinxcontrib-django?branch=master

sphinxcontrib-django
====================

Improvements for the output of Sphinx's autodoc for Django classes.

This adds the following improvements:

* Properly show which fields a model has.
* Properly show which fields a form has.
* Document the model fields as parameters in the model ``__init__()``.
* Link foreign key and related fields to the documentation of the referenced class.
* Hide irrelevant runtime information like ``declared_fieldsets``, ``fieldsets`` and ``Meta`` from classes.
* A ``:django:setting:`` role to allow linking to Django documentation. (e.g. *:django:setting:`SITE_ID`*)


Installation
------------

Usage:

.. code-block:: bash

    pip install sphinxcontrib-django

Add to the Sphinx config file (``conf.py``):

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        'sphinxcontrib_django',
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


Recommendations:
~~~~~~~~~~~~~~~~

When your project uses Celery, include `celery.contrib.sphinx`_ too.
This adds an ``autotask::`` directive, and ``:task:`app.tasks.my_task``` role.

Other great extensions are:

* sphinx-autodoc-annotation_: Converts Python 3 annotations to docstrings.
* ``sphinx.ext.graphviz``: Allows to create diagrams with ease.

An example configuration may look like:

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',         # The autodoc core
        'sphinx.ext.graphviz',        # Support creating charts!

        'celery.contrib.sphinx',      # Celery improvements!
        'sphinx_autodoc_annotation',  # Parses Python 3 annotations
        'sphinxcontrib_django',       # this module
    ]


.. _sphinx-autodoc-annotation: https://github.com/nicolashainaux/sphinx-autodoc-annotation
.. _celery.contrib.sphinx: http://docs.celeryproject.org/en/latest/reference/celery.contrib.sphinx.html
