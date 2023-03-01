import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_data(app, do_autodoc):
    options = {"members": None}
    actual = do_autodoc(app, "module", "dummy_django_app.settings", options)
    print(actual)
    assert list(actual) == [
        "",
        ".. py:module:: dummy_django_app.settings",
        "",
        "   Dummy Django settings file",
        "",
        "",
        ".. py:data:: INSTALLED_APPS",
        "   :module: dummy_django_app.settings",
        (
            "   :value: ['django.contrib.auth', 'django.contrib.contenttypes',"
            " 'dummy_django_app']"
        ),
        "",
        "   These are the installed apps",
        "",
        "   .. code-block:: JavaScript",
        "",
        (
            "       ['django.contrib.auth', 'django.contrib.contenttypes',"
            " 'dummy_django_app']\n"
        ),
        "",
    ]
