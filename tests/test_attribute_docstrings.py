import pytest

try:
    from phonenumber_field.modelfields import PhoneNumberField  # noqa: F401

    PHONENUMBER = True
except ModuleNotFoundError:
    # In case phonenumber is not used, pass
    PHONENUMBER = False


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.SimpleModel.dummy_field"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.dummy_field",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.CharField`",
        "",
        "   Very verbose name of dummy field. This should help you",
        "",
        "   Docstring of char field",
        "",
        "   .. warning::",
        "",
        "       Inline directives should be preserved.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey(app, do_autodoc):
    actual = do_autodoc(app, "attribute", "dummy_django_app.models.SimpleModel.file")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.file",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.FileModel`"
        ),
        "",
        (
            "   File (related name:"
            " :attr:`~dummy_django_app.models.FileModel.simple_models`)"
        ),
        "",
        "   Docstring of foreign key",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey_id(app, do_autodoc):
    actual = do_autodoc(app, "attribute", "dummy_django_app.models.SimpleModel.file_id")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.file_id",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Internal field, use :class:`~dummy_django_app.models.SimpleModel.file`"
            " instead."
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey_string(app, do_autodoc):
    actual = do_autodoc(app, "attribute", "dummy_django_app.models.SimpleModel.file")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.file",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.FileModel`"
        ),
        "",
        (
            "   File (related name:"
            " :attr:`~dummy_django_app.models.FileModel.simple_models`)"
        ),
        "",
        "   Docstring of foreign key",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey_string_abstract_model(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.AbstractModel.simple_model"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: AbstractModel.simple_model",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "",
        "   Simple model",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_foreignkey(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.FileModel.simple_models"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: FileModel.simple_models",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "",
        (
            "   All simple models of this file model (related name of"
            " :attr:`~dummy_django_app.models.SimpleModel.file`)"
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_manytomany_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.SimpleModel.childrenB"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.childrenB",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: :class:`~django.db.models.ManyToManyField` to"
            " :class:`~dummy_django_app.models.ChildModelB`"
        ),
        "",
        (
            "   ChildrenB (related name:"
            " :attr:`~dummy_django_app.models.ChildModelB.simple_models`)"
        ),
        "",
        "   Docstring of many to many field",
        "",
        "   .. note::",
        "",
        "       This syntax is also supported.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_manytomany_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChildModelB.simple_models"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChildModelB.simple_models",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: Reverse :class:`~django.db.models.ManyToManyField` from"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "",
        (
            "   All simple models of this child model b (related name of"
            " :attr:`~dummy_django_app.models.SimpleModel.childrenB`)"
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_onetoone_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChildModelA.simple_model"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChildModelA.simple_model",
        "   :module: dummy_django_app.models",
        "",
        (
            "   Type: Reverse :class:`~django.db.models.OneToOneField` from"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "",
        (
            "   The simple model of this child model a (related name of"
            " :attr:`~dummy_django_app.models.SimpleModel.childA`)"
        ),
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_generic_foreign_key(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.TaggedItem.content_object"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: TaggedItem.content_object",
        "   :module: dummy_django_app.models",
        "",
        "   Provide a generic many-to-one relation through the ``content_type`` and",
        "   ``object_id`` fields.",
        "",
        "   This class also doubles as an accessor to the related object (similar to",
        "   ForwardManyToOneDescriptor) by adding itself as a model attribute.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_manager_fields(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.SimpleModel.custom_objects"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: SimpleModel.custom_objects",
        "   :module: dummy_django_app.models",
        "   :value: <dummy_django_app.models.SimpleModelManager object>",
        "",
        "   Django manager to access the ORM",
        "   Use ``SimpleModel.objects.all()`` to fetch all objects.",
        "",
        "   Custom model manager",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_file_field(app, do_autodoc):
    actual = do_autodoc(app, "attribute", "dummy_django_app.models.FileModel.upload")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: FileModel.upload",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.FileField`",
        "",
        "   Upload",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_choice_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChoiceModel.choice_limit_below"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChoiceModel.choice_limit_below",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.IntegerField`",
        "",
        "   Choice limit below",
        "",
        "   Choices:",
        "",
        "   * ``0``",
        "   * ``1``",
        "   * ``2``",
        "   * ``3``",
        "   * ``4``",
        "   * ``5``",
        "   * ``6``",
        "   * ``7``",
        "   * ``8``",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_choice_field_limit_exact(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChoiceModel.choice_limit_exact"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChoiceModel.choice_limit_exact",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.IntegerField`",
        "",
        "   Choice limit exact",
        "",
        "   Choices:",
        "",
        "   * ``0``",
        "   * ``1``",
        "   * ``2``",
        "   * ``3``",
        "   * ``4``",
        "   * ``5``",
        "   * ``6``",
        "   * ``7``",
        "   * ``8``",
        "   * ``9``",
        "   * ``10``",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_choice_field_limit_above(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChoiceModel.choice_limit_above"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChoiceModel.choice_limit_above",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.IntegerField`",
        "",
        "   Choice limit above",
        "",
        "   Choices:",
        "",
        "   * ``0``",
        "   * ``1``",
        "   * ``2``",
        "   * ``3``",
        "   * ``4``",
        "   * ``5``",
        "   * ``6``",
        "   * ``7``",
        "   * ``8``",
        "   * ``9``",
        "   * and 2 more",
        "",
    ]


@pytest.mark.sphinx(
    "html", testroot="docstrings", confoverrides={"django_choices_to_show": 15}
)
def test_choice_field_custom_limit(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChoiceModel.choice_limit_above"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChoiceModel.choice_limit_above",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.IntegerField`",
        "",
        "   Choice limit above",
        "",
        "   Choices:",
        "",
        "   * ``0``",
        "   * ``1``",
        "   * ``2``",
        "   * ``3``",
        "   * ``4``",
        "   * ``5``",
        "   * ``6``",
        "   * ``7``",
        "   * ``8``",
        "   * ``9``",
        "   * ``10``",
        "   * ``11``",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_choice_field_empty(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChoiceModel.choice_with_empty"
    )
    print(actual)
    assert list(actual) == [
        "",
        ".. py:attribute:: ChoiceModel.choice_with_empty",
        "   :module: dummy_django_app.models",
        "",
        "   Type: :class:`~django.db.models.CharField`",
        "",
        "   Choice with empty",
        "",
        "   Choices:",
        "",
        "   * ``''`` (Empty string)",
        "   * ``Something``",
        "",
    ]


if PHONENUMBER:

    @pytest.mark.sphinx("html", testroot="docstrings")
    def test_phonenumber_field(app, do_autodoc):
        actual = do_autodoc(
            app, "attribute", "dummy_django_app.models.PhoneNumberModel.phone_number"
        )
        print(actual)
        assert list(actual) == [
            "",
            ".. py:attribute:: PhoneNumberModel.phone_number",
            "   :module: dummy_django_app.models",
            "",
            "   Type: :class:`~phonenumber_field.modelfields.PhoneNumberField`",
            "",
            "   Phone number",
            "",
        ]
