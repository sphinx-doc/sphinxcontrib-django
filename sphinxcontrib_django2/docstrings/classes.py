"""
This module contains all functions which are used to improve the documentation of classes.
"""

from django import forms
from django.db import models

from .field_utils import get_field_type, get_field_verbose_name


def improve_class_docstring(app, cls, lines):
    """
    Improve the documentation of a class if it's a Django model or form

    :param app: The Sphinx application object
    :type app: ~sphinx.application.Sphinx

    :param cls: The instance of the class to document
    :type cls: object

    :param lines: The docstring lines
    :type lines: list [ str ]
    """
    if issubclass(cls, models.Model):
        improve_model_docstring(app, cls, lines)
    elif issubclass(cls, forms.BaseForm):
        improve_form_docstring(cls, lines)


def improve_model_docstring(app, model, lines):
    """
    Improve the documentation of a Django :class:`~django.db.models.Model` subclass.

    This adds all model fields as parameters to the ``__init__()`` method.

    :param app: The Sphinx application object
    :type app: ~sphinx.application.Sphinx

    :param model: The instance of the model to document
    :type model: ~django.db.models.Model

    :param lines: The docstring lines
    :type lines: list [ str ]
    """

    # Add database table name
    if app.config.django_show_db_tables:
        lines.insert(0, "")
        lines.insert(0, f"**Database table:** ``{model._meta.db_table}``")

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

    # Add the normal fields to the docstring
    add_model_parameters(non_related_fields, lines)

    # Add the related fields
    if related_fields:
        lines.append("")
        lines.append("Relationship fields:")
        lines.append("")
        add_model_parameters(related_fields, lines)

    # Add the reverse related fields
    if reverse_related_fields:
        lines.append("")
        lines.append("Reverse relationships:")
        lines.append("")
        add_model_parameters(reverse_related_fields, lines)

    # Add the inheritance diagram
    if (
        "sphinx.ext.inheritance_diagram" in app.extensions
        and "sphinx.ext.graphviz" in app.extensions
        and not any("inheritance-diagram::" in line for line in lines)
    ):
        lines.append(".. inheritance-diagram::")  # pragma: no cover


def add_model_parameters(fields, lines):
    """
    Add the given fields as model parameter with the ``:param:`` directive

    :param fields: The list of fields
    :type fields: list [ ~django.db.models.Field ]

    :param lines: The list of current docstring lines
    :type lines: list [ str ]
    """
    for field in fields:
        # Add verbose name
        lines.append(f":param {field.name}: {get_field_verbose_name(field)}")

        # Add type
        lines.append(f":type {field.name}: {get_field_type(field, include_role=False)}")


def improve_form_docstring(form, lines):
    """
    Improve the documentation of a Django :class:`~django.forms.Form` class.
    This highlights the available fields in the form.

    :param form: The form object
    :type form: ~django.forms.Form

    :param lines: The list of existing docstring lines
    :type lines: list [ str ]
    """
    lines.append("**Form fields:**")
    lines.append("")
    for name, field in form.base_fields.items():
        field_type = f"{field.__class__.__module__}.{field.__class__.__name__}"
        label = field.label or name.replace("_", " ").title()
        lines.append(f"* ``{name}``: {label} (:class:`~{field_type}`)")
