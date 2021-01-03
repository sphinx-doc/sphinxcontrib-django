import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_simple_model(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.SimpleModel")
    print(actual)
    assert actual == [
        "",
        ".. py:class:: SimpleModel(id, foreignkey, onetoonefield, dummy_field)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Id",
        "   :type id: AutoField",
        "   :param foreignkey: Foreignkey",
        "   :type foreignkey: ForeignKey to :class:`~dummy_django_app.models.FileModel`",
        "   :param onetoonefield: Onetoonefield",
        "   :type onetoonefield: OneToOneField to :class:`~dummy_django_app.models.ChildModel`",
        "   :param dummy_field: Very verbose name of dummy field. This should help you",
        "   :type dummy_field: CharField",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_abstract_model(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.AbstractModel")
    print(actual)
    assert actual == [
        "",
        ".. py:class:: AbstractModel(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "   :param foreignkey_string: Foreignkey string",
        "   :type foreignkey_string: ForeignKey to :class:`~dummy_django_app.models.SimpleModel`",
        "   :param foreignkey_string_containing_dot: Foreignkey string containing dot",
        "   :type foreignkey_string_containing_dot: ForeignKey to "
        ":class:`~django.contrib.auth.models.User`",
        "   :param foreignkey_string_self: Foreignkey string self",
        "   :type foreignkey_string_self: ForeignKey to "
        ":class:`~dummy_django_app.models.AbstractModel`",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_form(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.forms.SimpleForm")
    print(actual)
    assert actual == [
        "",
        ".. py:class:: SimpleForm(*args, **kwargs)",
        "   :module: dummy_django_app.forms",
        "",
        "   **Form fields:**",
        "",
        "   * ``foreignkey``: Foreignkey (:class:`~django.forms.ModelChoiceField`)",
        "   * ``dummy_field``: Very verbose name of dummy field "
        "(:class:`~django.forms.CharField`)",
        "   * ``test1``: Test1 (:class:`~django.forms.CharField`)",
        "   * ``test2``: Test2 (:class:`~django.forms.CharField`)",
        "",
    ]
