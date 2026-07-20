from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.conf import settings
from django.db.models import AutoField

if TYPE_CHECKING:
    from collections.abc import Callable

    from docutils.statemachine import StringList
    from sphinx.testing.util import SphinxTestApp


def autofield() -> str:
    return getattr(
        settings,
        "DEFAULT_AUTO_FIELD",
        f"{AutoField.__module__}.{AutoField.__qualname__}",
    )


@pytest.mark.sphinx("html", testroot="docstrings")
def test_simple_model(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    actual = do_autodoc(app, "class", "dummy_django_app.models.SimpleModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: SimpleModel(id, file, childA, dummy_field)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        f"   :type id: ~{autofield()}",
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
def test_database_table(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
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
        f"   :type id: ~{autofield()}",
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
def test_abstract_model(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
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
def test_abstract_model_with_tables_names_and_ignore_abstract(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
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
def test_abstract_model_with_tables_names_and_abstract_show(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
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
def test_bare_model_class(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    """
    Regression test: Sphinx >= 9 emits ``autodoc-process-docstring`` for the bare
    :class:`~django.db.models.Model` class itself (e.g. as the bound of a PEP 695 type
    parameter), which has no ``_meta`` unlike its concrete subclasses.
    """
    actual = do_autodoc(app, "class", "django.db.models.Model")
    print(actual)
    assert list(actual)[:3] == [
        "",
        ".. py:class:: Model(*args, **kwargs)",
        "   :module: django.db.models",
    ]


@pytest.mark.sphinx("html", testroot="docstrings")
def test_file_model(app: SphinxTestApp, do_autodoc: Callable[..., StringList]) -> None:
    actual = do_autodoc(app, "class", "dummy_django_app.models.FileModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: FileModel(id, upload)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        f"   :type id: ~{autofield()}",
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
def test_tagged_item(app: SphinxTestApp, do_autodoc: Callable[..., StringList]) -> None:
    actual = do_autodoc(app, "class", "dummy_django_app.models.TaggedItem")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: TaggedItem(id, tag, content_type, object_id)",
        "   :module: dummy_django_app.models",
        "",
        "   :param id: Primary key: ID",
        f"   :type id: ~{autofield()}",
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
def test_form(app: SphinxTestApp, do_autodoc: Callable[..., StringList]) -> None:
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


@pytest.mark.sphinx("html", testroot="docstrings")
def test_relation_model(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    actual = do_autodoc(app, "class", "dummy_django_app2.models.GenericRelationModel")
    print(actual)
    assert list(actual) == [
        "",
        ".. py:class:: GenericRelationModel(id)",
        "   :module: dummy_django_app2.models",
        "",
        "   :param id: Primary key: ID",
        f"   :type id: ~{autofield()}",
        "",
        "   Relationship fields:",
        "",
        "   :param relation_field: Relation field",
        (
            "   :type relation_field:"
            " :class:`~django.contrib.contenttypes.fields.GenericRelation` to"
            " :class:`~dummy_django_app.models.TaggedItem`"
        ),
        "",
        "   .. inheritance-diagram:: dummy_django_app2.models.GenericRelationModel",
        "",
    ]
