import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_django_configured(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.MonkeyPatched")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: MonkeyPatched(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "   Monkeypatched docstring",
        "",
        "   :param id: Primary key: ID",
        "   :type id: ~django.db.models.AutoField",
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.MonkeyPatched",
        "",
    ]
