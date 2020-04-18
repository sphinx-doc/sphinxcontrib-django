Changelog
=========

Version 0.6.0 (unreleased)
--------------------------

* Drop Python 2, Django 1.11 support

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
