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
    assert actual == [
        "",
        ".. py:attribute:: SimpleModel.dummy_field",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** Very verbose name of dummy field",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.SimpleModel.foreignkey"
    )
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: SimpleModel.foreignkey",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** foreignkey, accesses the "
        ":class:`~dummy_django_app.models.FileModel` model.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_foreignkey_string(app, do_autodoc):
    actual = do_autodoc(
        app,
        "attribute",
        "dummy_django_app.models.AbstractModel.foreignkey_string",
    )
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: AbstractModel.foreignkey_string",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** foreignkey string, accesses the :class:`~SimpleModel` model.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_foreignkey(app, do_autodoc):
    actual = do_autodoc(
        app,
        "attribute",
        "dummy_django_app.models.FileModel.reverse_foreignkey",
    )
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: FileModel.reverse_foreignkey",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** foreignkey, accesses the M2M "
        ":class:`~dummy_django_app.models.SimpleModel` model.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_onetoone_field(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.ChildModel.reverse_onetoonefield"
    )
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: ChildModel.reverse_onetoonefield",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** onetoonefield, accesses the "
        ":class:`~dummy_django_app.models.SimpleModel` model.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_manager_fields(app, do_autodoc):
    actual = do_autodoc(
        app, "attribute", "dummy_django_app.models.SimpleModel.custom_objects"
    )
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: SimpleModel.custom_objects",
        "   :module: dummy_django_app.models",
        "   :value: <dummy_django_app.models.SimpleModelManager object>",
        "",
        "   Custom model manager",
        "",
        "   Django manager to access the ORM",
        "   Use ``SimpleModel.objects.all()`` to fetch all objects.",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_file_field(app, do_autodoc):
    actual = do_autodoc(app, "attribute", "dummy_django_app.models.FileModel.file")
    print(actual)
    assert actual == [
        "",
        ".. py:attribute:: FileModel.file",
        "   :module: dummy_django_app.models",
        "",
        "   **Model field:** file",
        "   **Return type:** :class:`~django.db.models.fields.files.FieldFile`",
        "",
    ]


if PHONENUMBER:

    @pytest.mark.sphinx("html", testroot="docstrings")
    def test_phonenumber_field(app, do_autodoc):
        actual = do_autodoc(
            app, "attribute", "dummy_django_app.models.PhoneNumberModel.phone_number"
        )
        print(actual)
        assert actual == [
            "",
            ".. py:attribute:: PhoneNumberModel.phone_number",
            "   :module: dummy_django_app.models",
            "",
            "   **Model field:** phone number",
            "   **Return type:** :class:`~phonenumber_field.phonenumber.PhoneNumber`",
            "",
        ]
