"""
This module contains utility functions for fields which are used by both the
:mod:`~sphinxcontrib_django.docstrings.attributes` and
:mod:`~sphinxcontrib_django.docstrings.classes` modules.
"""
from __future__ import annotations

from django.apps import apps
from django.contrib import contenttypes
from django.db import models
from django.utils.encoding import force_str


def get_field_type(field: models.Field, include_role: bool = True) -> str:
    """
    Get the type of a field including the correct intersphinx mappings.

    :param field: The field
    :param include_directive: Whether or not the role :any:`py:class` should be included
    :return: The type of the field
    """
    if isinstance(field, models.fields.related.RelatedField):
        to = field.remote_field.model
        if isinstance(to, str):
            # This happens with foreign keys of abstract models
            to = get_model_from_string(field, to)
        return (
            f":class:`~{type(field).__module__}.{type(field).__name__}` to"
            f" :class:`~{to.__module__}.{to.__name__}`"
        )
    if isinstance(field, models.fields.reverse_related.ForeignObjectRel):
        to = field.remote_field.model
        return (
            "Reverse"
            f" :class:`~{type(field.remote_field).__module__}.{type(field.remote_field).__name__}`"
            f" from :class:`~{to.__module__}.{to.__name__}`"
        )
    if include_role:
        # For the docstrings of attributes, the :class: role is required
        return f":class:`~{type(field).__module__}.{type(field).__name__}`"

    # For the :param: role in class docstrings, the :class: role is not required
    return f"~{type(field).__module__}.{type(field).__name__}"


def get_field_verbose_name(field: models.Field) -> str:
    """
    Get the verbose name of the field.
    If the field has a ``help_text``, it is also included.

    In case the field is a related field, the ``related_name`` is used to link to the remote model.
    For reverse related fields, the originating field is linked.

    :param field: The field
    """
    help_text = ""
    # Check whether the field is a reverse related field
    if isinstance(field, models.fields.reverse_related.ForeignObjectRel):
        # Convert related name to a readable name if ``snake_case`` is used
        related_name = (
            field.related_name.replace("_", " ") if field.related_name else None
        )
        if isinstance(field, models.fields.reverse_related.OneToOneRel):
            # If a related name is given, use it, else use the verbose name of the remote model
            related_name = related_name or field.remote_field.model._meta.verbose_name
            # If field is a OneToOne field, use the prefix "The"
            verbose_name = (
                f"The {related_name} of this {field.model._meta.verbose_name}"
            )
        else:
            # This means field is an instance of ManyToOneRel or ManyToManyRel
            # If a related name is given, use it, else use the verbose name of the remote model
            related_name = (
                related_name or field.remote_field.model._meta.verbose_name_plural
            )
            # If field is a foreign key or a ManyToMany field, use the prefix "All"
            verbose_name = (
                f"All {related_name} of this {field.model._meta.verbose_name}"
            )
        # Link to the origin of the reverse related field if it's not from an abstract model
        if not field.remote_field.model._meta.abstract:
            verbose_name += (
                f" (related name of :attr:`~{field.remote_field.model.__module__}"
                f".{field.remote_field.model.__name__}.{field.remote_field.name}`)"
            )
    elif hasattr(contenttypes, "fields") and isinstance(
        field, contenttypes.fields.GenericForeignKey
    ):
        # GenericForeignKey does not inherit from django.db.models.Field and has no verbose_name
        return (
            "Generic foreign key to the"
            " :class:`~django.contrib.contenttypes.models.ContentType` specified in"
            f" :attr:`~{field.model.__module__}.{field.model.__name__}.{field.ct_field}`"
        )
    else:
        # This means the field is either a normal field or a forward related field
        # If the field is a primary key, include a notice
        primary_key = "Primary key: " if field.primary_key else ""

        field_verbose_name = force_str(field.verbose_name)
        # Make the first letter upper case while leave the rest unchanged
        # (str.capitalize() would make the rest lower case, e.g. ID => Id)
        verbose_name = (
            primary_key + field_verbose_name[:1].upper() + field_verbose_name[1:]
        )
        help_text = force_str(field.help_text)

    # Add help text if field has one
    if help_text:
        # Separate verbose name and help text by a dot
        if not verbose_name.endswith("."):
            verbose_name += ". "
        verbose_name += help_text

    if isinstance(field, models.fields.related.RelatedField):
        # If field is a forward related field, reference the remote model
        to = field.remote_field.model
        if isinstance(to, str):
            # This happens with foreign keys of abstract models
            to = get_model_from_string(field, to)
        # If a related name is defined
        if hasattr(field.remote_field, "related_name"):
            related_name = (
                field.remote_field.related_name or field.model.__name__.lower()
            )

        # Link to the related field if it's not an abstract model
        if not field.model._meta.abstract:
            verbose_name += (
                " (related name:"
                f" :attr:`~{to.__module__}.{to.__name__}.{related_name}`)"
            )
    return verbose_name


def get_model_from_string(field: models.Field, model_string: str) -> type[models.Model]:
    """
    Get a model class from a string

    :param field: The field
    :param model_string: The string label of the model
    :return: The class of the model
    """
    if "." in model_string:
        model = apps.get_model(model_string)
    elif model_string == "self":
        model = field.model
    else:
        model = apps.get_model(field.model._meta.app_label, model_string)
    return model
