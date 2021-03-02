import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_exclude_members(app, do_autodoc):
    options = {"members": None, "undoc-members": None}
    assert not any(
        "base_fields" in line
        for line in do_autodoc(app, "module", "dummy_django_app.forms", options)
    )


@pytest.mark.sphinx("html", testroot="docstrings")
def test_include_members(app, do_autodoc):
    options = {"members": None}
    assert any(
        "__init__" in line
        for line in do_autodoc(app, "module", "dummy_django_app.forms", options)
    )
