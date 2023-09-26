import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_simple_model(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.SimpleModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: SimpleModel(id, file, childA, dummy_field)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        "   :type id: ~django.db.models.AutoField",
        "   :param dummy_field: Very verbose name of dummy field. This should help you",
        "",
        "                       Docstring of char field",
        "",
        "                       .. warning::",
        "",
        "                           Inline directives should be preserved.",
        "",
        "   :type dummy_field: ~django.db.models.CharField",
        "",
        "   Relationship fields:",
        "",
        (
            "   :param file: File (related name:"
            " :attr:`~dummy_django_app.models.FileModel.simple_models`)"
        ),
        "",
        "                Docstring of foreign key",
        "",
        (
            "   :type file: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.FileModel`"
        ),
        (
            "   :param childA: ChildA (related name:"
            " :attr:`~dummy_django_app.models.ChildModelA.simple_model`)"
        ),
        "",
        "                  Docstring of one to one field",
        "",
        (
            "   :type childA: :class:`~django.db.models.OneToOneField` to"
            " :class:`~dummy_django_app.models.ChildModelA`"
        ),
        (
            "   :param childrenB: ChildrenB (related name:"
            " :attr:`~dummy_django_app.models.ChildModelB.simple_models`)"
        ),
        "",
        "                     Docstring of many to many field",
        "",
        "                     .. note::",
        "",
        "                         This syntax is also supported.",
        "",
        (
            "   :type childrenB: :class:`~django.db.models.ManyToManyField` to"
            " :class:`~dummy_django_app.models.ChildModelB`"
        ),
        "",
        "   Reverse relationships:",
        "",
        (
            "   :param childmodela: All child model as of this simple model (related"
            " name of :attr:`~dummy_django_app.models.ChildModelA.simple_model`)"
        ),
        (
            "   :type childmodela: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.ChildModelA`"
        ),
        (
            "   :param childmodelb: All child model bs of this simple model (related"
            " name of :attr:`~dummy_django_app.models.ChildModelB.simple_model`)"
        ),
        (
            "   :type childmodelb: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.ChildModelB`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.SimpleModel",
        "",
    ]


@pytest.mark.sphinx(
    "html", testroot="docstrings", confoverrides={"django_show_db_tables": True}
)
def test_database_table(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.SimpleModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: SimpleModel(id, file, childA, dummy_field)",
        "   :module: dummy_django_app.models",
        "",
        "   **Database table:** ``dummy_django_app_simplemodel``",
        "",
        "   :param id: Primary key: ID",
        "   :type id: ~django.db.models.AutoField",
        "   :param dummy_field: Very verbose name of dummy field. This should help you",
        "",
        "                       Docstring of char field",
        "",
        "                       .. warning::",
        "",
        "                           Inline directives should be preserved.",
        "",
        "   :type dummy_field: ~django.db.models.CharField",
        "",
        "   Relationship fields:",
        "",
        (
            "   :param file: File (related name:"
            " :attr:`~dummy_django_app.models.FileModel.simple_models`)"
        ),
        "",
        "                Docstring of foreign key",
        "",
        (
            "   :type file: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.FileModel`"
        ),
        (
            "   :param childA: ChildA (related name:"
            " :attr:`~dummy_django_app.models.ChildModelA.simple_model`)"
        ),
        "",
        "                  Docstring of one to one field",
        "",
        (
            "   :type childA: :class:`~django.db.models.OneToOneField` to"
            " :class:`~dummy_django_app.models.ChildModelA`"
        ),
        (
            "   :param childrenB: ChildrenB (related name:"
            " :attr:`~dummy_django_app.models.ChildModelB.simple_models`)"
        ),
        "",
        "                     Docstring of many to many field",
        "",
        "                     .. note::",
        "",
        "                         This syntax is also supported.",
        "",
        (
            "   :type childrenB: :class:`~django.db.models.ManyToManyField` to"
            " :class:`~dummy_django_app.models.ChildModelB`"
        ),
        "",
        "   Reverse relationships:",
        "",
        (
            "   :param childmodela: All child model as of this simple model (related"
            " name of :attr:`~dummy_django_app.models.ChildModelA.simple_model`)"
        ),
        (
            "   :type childmodela: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.ChildModelA`"
        ),
        (
            "   :param childmodelb: All child model bs of this simple model (related"
            " name of :attr:`~dummy_django_app.models.ChildModelB.simple_model`)"
        ),
        (
            "   :type childmodelb: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.ChildModelB`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.SimpleModel",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_abstract_model(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.AbstractModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: AbstractModel(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "",
        "   Relationship fields:",
        "",
        "   :param simple_model: Simple model",
        (
            "   :type simple_model: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "   :param user: User",
        (
            "   :type user: :class:`~django.db.models.ForeignKey` to"
            " :class:`~django.contrib.auth.models.User`"
        ),
        "   :param foreignkey_self: Foreignkey self",
        (
            "   :type foreignkey_self: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.AbstractModel`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.AbstractModel",
        "",
    ]


@pytest.mark.sphinx(
    "html", testroot="docstrings", confoverrides={"django_show_db_tables": True}
)
def test_abstract_model_with_tables_names_and_ignore_abstract(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.AbstractModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: AbstractModel(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "",
        "   Relationship fields:",
        "",
        "   :param simple_model: Simple model",
        (
            "   :type simple_model: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "   :param user: User",
        (
            "   :type user: :class:`~django.db.models.ForeignKey` to"
            " :class:`~django.contrib.auth.models.User`"
        ),
        "   :param foreignkey_self: Foreignkey self",
        (
            "   :type foreignkey_self: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.AbstractModel`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.AbstractModel",
        "",
    ]


@pytest.mark.sphinx(
    "html",
    testroot="docstrings",
    confoverrides={
        "django_show_db_tables": True,
        "django_show_db_tables_abstract": True,
    },
)
def test_abstract_model_with_tables_names_and_abstract_show(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.AbstractModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: AbstractModel(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "   **Database table:** ``None``",
        "",
        "",
        "   Relationship fields:",
        "",
        "   :param simple_model: Simple model",
        (
            "   :type simple_model: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "   :param user: User",
        (
            "   :type user: :class:`~django.db.models.ForeignKey` to"
            " :class:`~django.contrib.auth.models.User`"
        ),
        "   :param foreignkey_self: Foreignkey self",
        (
            "   :type foreignkey_self: :class:`~django.db.models.ForeignKey` to"
            " :class:`~dummy_django_app.models.AbstractModel`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.AbstractModel",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_file_model(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.FileModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: FileModel(id, upload)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        "   :type id: ~django.db.models.AutoField",
        "   :param upload: Upload",
        "   :type upload: ~django.db.models.FileField",
        "",
        "   Reverse relationships:",
        "",
        (
            "   :param simple_models: All simple models of this file model (related"
            " name of :attr:`~dummy_django_app.models.SimpleModel.file`)"
        ),
        (
            "   :type simple_models: Reverse :class:`~django.db.models.ForeignKey` from"
            " :class:`~dummy_django_app.models.SimpleModel`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.FileModel",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_tagged_item(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.models.TaggedItem")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: TaggedItem(id, tag, content_type, object_id)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        "   :type id: ~django.db.models.AutoField",
        "   :param tag: Tag",
        "   :type tag: ~django.db.models.SlugField",
        "   :param object_id: Object id",
        "   :type object_id: ~django.db.models.PositiveIntegerField",
        (
            "   :param content_object: Generic foreign key to the"
            " :class:`~django.contrib.contenttypes.models.ContentType` specified in"
            " :attr:`~dummy_django_app.models.TaggedItem.content_type`"
        ),
        (
            "   :type content_object:"
            " ~django.contrib.contenttypes.fields.GenericForeignKey"
        ),
        "",
        "   Relationship fields:",
        "",
        (
            "   :param content_type: Content type (related name:"
            " :attr:`~django.contrib.contenttypes.models.ContentType.taggeditem`)"
        ),
        (
            "   :type content_type: :class:`~django.db.models.ForeignKey` to"
            " :class:`~django.contrib.contenttypes.models.ContentType`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.TaggedItem",
        "",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_form(app, do_autodoc):
    actual = do_autodoc(app, "class", "dummy_django_app.forms.SimpleForm")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: SimpleForm(*args, **kwargs)",
        "   :module: dummy_django_app.forms",
        "",
        "   **Form fields:**",
        "",
        "   * ``file``: File (:class:`~django.forms.ModelChoiceField`)",
        "   * ``childA``: ChildA (:class:`~django.forms.ModelChoiceField`)",
        (
            "   * ``childrenB``: ChildrenB"
            " (:class:`~django.forms.ModelMultipleChoiceField`)"
        ),
        (
            "   * ``dummy_field``: Very verbose name of dummy field"
            " (:class:`~django.forms.CharField`)"
        ),
        "   * ``test1``: Test1 (:class:`~django.forms.CharField`)",
        "   * ``test2``: Test2 (:class:`~django.forms.CharField`)",
        "",
    ]
