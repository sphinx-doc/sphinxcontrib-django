import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_method_display(app, do_autodoc):
    actual = do_autodoc(
        app, "method", "dummy_django_app.models.SimpleModel.get_dummy_field_display"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:method:: SimpleModel.get_dummy_field_display()",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Shows the label of the :attr:`dummy_field`. See"
            " :meth:`~django.db.models.Model.get_FOO_display` for more information."
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_method_get_next_by(app, do_autodoc):
    actual = do_autodoc(
        app, "method", "dummy_django_app.models.SimpleModel.get_next_by_dummy_field"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:method:: SimpleModel.get_next_by_dummy_field()",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Finds next instance based on :attr:`dummy_field`. See"
            " :meth:`~django.db.models.Model.get_next_by_FOO` for more information."
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_method_get_previous_by(app, do_autodoc):
    actual = do_autodoc(
        app, "method", "dummy_django_app.models.SimpleModel.get_previous_by_dummy_field"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:method:: SimpleModel.get_previous_by_dummy_field()",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Finds previous instance based on :attr:`dummy_field`. See"
            " :meth:`~django.db.models.Model.get_previous_by_FOO` for more information."
        ),
        "",
    ]
