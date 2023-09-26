"""
This module contains all functions which are used to improve the documentation of classes.
"""
from __future__ import annotations

from django import forms
from django.db import models
from sphinx.application import Sphinx
from sphinx.pycode import ModuleAnalyzer

from .field_utils import get_field_type, get_field_verbose_name


def improve_class_docstring(app: Sphinx, cls: type, lines: list[str]) -> None:
    """
    Improve the documentation of a class if it's a Django model or form

    :param app: The Sphinx application object
    :param cls: The instance of the class to document
    :param lines: The docstring lines
    """
    if issubclass(cls, models.Model):
        improve_model_docstring(app, cls, lines)
    elif issubclass(cls, forms.BaseForm):
        improve_form_docstring(cls, lines)


def improve_model_docstring(app: Sphinx, model: models.Model, lines: list[str]) -> None:
    """
    Improve the documentation of a Django :class:`~django.db.models.Model` subclass.

    This adds all model fields as parameters to the ``__init__()`` method.

    :param app: The Sphinx application object
    :param model: The instance of the model to document
    :param lines: The docstring lines
    """

    # Add database table name
    if app.config.django_show_db_tables:
        add_db_table_name(app, model, lines)

    # Get predefined params to exclude them from the automatically inserted params
    param_offset = len(":param ")
    predefined_params = [
        line[param_offset : line.find(":", param_offset)]
        for line in lines
        if line.startswith(":param ") and ":" in line[param_offset:]
    ]

    # Get all fields of this model which are not already explicitly included in the docstring
    all_fields = [
        field
        for field in model._meta.get_fields(include_parents=True)
        if field.name not in predefined_params
    ]
    # Get all related fields (ForeignKey, OneToOneField, ManyToManyField)
    related_fields = [
        field
        for field in all_fields
        if isinstance(field, models.fields.related.RelatedField)
    ]
    # Get all reverse relationships
    reverse_related_fields = [
        field
        for field in all_fields
        if isinstance(field, models.fields.reverse_related.ForeignObjectRel)
    ]
    # All fields which are neither related nor reverse related
    non_related_fields = [
        field
        for field in all_fields
        if field not in related_fields + reverse_related_fields
    ]

    # Analyze model to get inline field docstrings
    analyzer = ModuleAnalyzer.for_module(model.__module__)
    analyzer.analyze()
    field_docs = {
        field_name: field_docstring
        for (_, field_name), field_docstring in analyzer.attr_docs.items()
    }

    # Add the normal fields to the docstring
    add_model_parameters(non_related_fields, lines, field_docs)

    # Add the related fields
    if related_fields:
        lines.append("")
        lines.append("Relationship fields:")
        lines.append("")
        add_model_parameters(related_fields, lines, field_docs)

    # Add the reverse related fields
    if reverse_related_fields:
        lines.append("")
        lines.append("Reverse relationships:")
        lines.append("")
        add_model_parameters(reverse_related_fields, lines, field_docs)

    # Add the inheritance diagram
    if (
        "sphinx.ext.inheritance_diagram" in app.extensions
        and "sphinx.ext.graphviz" in app.extensions
        and not any("inheritance-diagram::" in line for line in lines)
    ):
        lines.append("")
        lines.append(f".. inheritance-diagram:: {model.__module__}.{model.__name__}")
        lines.append("")


def add_db_table_name(app: Sphinx, model: models.Model, lines: list[str]) -> None:
    """
    Format and add table name by extension configuration.

    :param app: The Sphinx application object
    :param model: The instance of the model to document
    :param lines: The docstring lines
    """
    if model._meta.abstract and not app.config.django_show_db_tables_abstract:
        return

    table_name = None if model._meta.abstract else model._meta.db_table
    lines.insert(0, "")
    lines.insert(0, f"**Database table:** ``{table_name}``")


def add_model_parameters(
    fields: list[models.Field], lines: list[str], field_docs: dict
) -> None:
    """
    Add the given fields as model parameter with the ``:param:`` directive

    :param fields: The list of fields
    :param lines: The list of current docstring lines
    :param field_docs: The attribute docstrings of the model
    """
    for field in fields:
        # Add docstrings if they are found
        docstring_lines = field_docs.get(field.name, [])
        # Add param doc line
        param = f":param {field.name}: "
        lines.append(param + get_field_verbose_name(field))
        if docstring_lines:
            # Separate from verbose name
            lines.append("")
        # Add and indent existing docstring lines
        lines.extend([(" " * len(param)) + line for line in docstring_lines])

        # Add type
        lines.append(f":type {field.name}: {get_field_type(field, include_role=False)}")


def improve_form_docstring(form: forms.Form, lines: list[str]) -> None:
    """
    Improve the documentation of a Django :class:`~django.forms.Form` class.
    This highlights the available fields in the form.

    :param form: The form object
    :param lines: The list of existing docstring lines
    """
    lines.append("**Form fields:**")
    lines.append("")
    for name, field in form.base_fields.items():
        field_type = f"{field.__class__.__module__}.{field.__class__.__name__}"
        label = field.label or name.replace("_", " ").title()
        lines.append(f"* ``{name}``: {label} (:class:`~{field_type}`)")
