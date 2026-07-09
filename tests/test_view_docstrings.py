import importlib

import pytest
from django.test import override_settings

from sphinxcontrib_django.docstrings.views import improve_view_docstring


@pytest.mark.sphinx("html", testroot="docstrings")
def test_view_url_paths(app, do_autodoc):
    actual = do_autodoc(app, "function", "dummy_django_app.views.simple_view")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:function:: simple_view(request)",
        "   :module: dummy_django_app.views",
        "",
        "   A simple view function.",
        "",
        "   URL paths:",
        "",
        "   * ``/simple/``",
        "   * ``/simple/<year>/``",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_function_without_url_unchanged(app, do_autodoc):
    actual = do_autodoc(app, "function", "dummy_django_app.views.not_a_view")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:function:: not_a_view()",
        "   :module: dummy_django_app.views",
        "",
        "   A function which is not mapped to any URL.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_no_root_urlconf_leaves_docstring_unchanged(app):
    simple_view = importlib.import_module("dummy_django_app.views").simple_view
    lines = ["A simple view function."]
    with override_settings(ROOT_URLCONF=None):
        improve_view_docstring(simple_view, lines)
    assert lines == ["A simple view function."]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_appends_blank_line_before_url_paths_section(app):
    simple_view = importlib.import_module("dummy_django_app.views").simple_view
    lines = ["A simple view function."]
    improve_view_docstring(simple_view, lines)
    assert lines == [
        "A simple view function.",
        "",
        "URL paths:",
        "",
        "* ``/simple/``",
        "* ``/simple/<year>/``",
    ]
