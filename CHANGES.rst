Changelog
=========

UNRELEASED
----------

* Add support for Python 3.9


Version 1.0.2 (2021-02-02)
--------------------------

* Add support for GenericForeignKey field of django.contrib.contenttypes


Version 1.0.1 (2021-02-02)
--------------------------

* Fix Intersphinx mappings to AppConfig and Manager classes


Version 1.0 (2021-01-24)
------------------------

* Fix more Intersphinx mappings to Django classes
* Refactor package structure
* Refactor tests
* Improve docstring output
* Improve handling of related and reverse related fields
* Add documentation for sphinxcontrib_django2 itself
* Improve docstrings of iterable data
* Add config value for Django settings
* Load autodoc and intersphinx extensions in setup()
* Provide default intersphinx_mapping
* Return extension metadata in setup()
* Move dev dependencies from Pipfile to setup.py
* Add readthedocs.io integration

Version 0.7 (2020-11-30)
------------------------

* Fix Intersphinx mappings to Django classes
* 100% test coverage


Version 0.6 (2020-11-16)
--------------------------

* Fix deferred attribute for Django >=2.1, <3.0
* Django: Drop support for [1.11, 2.0], add support for [2.2, 3.0, 3.1]
* Python: Drop support for [2.7, 3.5], add support for [3.6, 3.7, 3.8]
* Replace force_text by force_str (deprecated in Django 4.0)
* Improved test coverage
* Support for Django ModelFields


Version 0.5.1 (2020-01-26)
--------------------------

* Fix deferred attribute for Django 3.0.


Version 0.5 (2019-08-09)
------------------------

* Model fields always show verbose name if present.
* Model fields are skipped when they are already documented.
* Support "self" in foreign keys.
* Allow ``:setting:`` registration to fail
* Fixed ``runtests.py`` for Django 2.2
* Reformatted all source code with black, isort and flake8


Version 0.4 (2018-07-26)
------------------------

* Fixed Django 2.0 behavior when foreignkeys are strings.


Version 0.3.1 (2018-03-11)
--------------------------

* Fixed Python 2 issue with ``list.clear()``.


Version 0.3 (2018-02-19)
------------------------

* Fixed Django 2.0 support
* Fixed missing form fields
* Fixed handling of ``ForeignKey('modelname')``


Version 0.2.1 (2018-01-02)
------------------------

* Fixed bad packaging of 0.2


Version 0.2 (2018-01-02)
------------------------

* Support more Python versions (removed f-strings)


version 0.1 (2017-12-07)
------------------------

* Initial version
