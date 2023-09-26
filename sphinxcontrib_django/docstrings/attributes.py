"""
This module contains all functions which are used to improve the documentation of attributes.
"""
from __future__ import annotations

from django.db import models
from django.db.models.fields import related_descriptors
from django.db.models.fields.files import FileDescriptor
from django.db.models.manager import ManagerDescriptor
from django.db.models.query_utils import DeferredAttribute
from django.utils.module_loading import import_string
from sphinx.util.docstrings import prepare_docstring

from .field_utils import get_field_type, get_field_verbose_name

FIELD_DESCRIPTORS = (FileDescriptor, related_descriptors.ForwardManyToOneDescriptor)

# Support for some common third party fields
try:
    from phonenumber_field.modelfields import PhoneNumberDescriptor

    FIELD_DESCRIPTORS += (PhoneNumberDescriptor,)
except ImportError:
    PhoneNumberDescriptor = None


def improve_attribute_docstring(app, attribute, name, lines):
    """
    Improve the documentation of various model fields.

    This improves the navigation between related objects.

    :param app: The Sphinx application object
    :type app: ~sphinx.application.Sphinx

    :param attribute: The instance of the object to document
    :type attribute: object

    :param name: The full dotted path to the object
    :type name: str

    :param lines: The docstring lines
    :type lines: list [ str ]
    """
    # Save initial docstring lines to append them to the modified lines
    docstring_lines = lines.copy()
    lines.clear()
    if isinstance(attribute, DeferredAttribute):
        # This only points to a field name, not a field.
        # Get the field by importing the name.
        cls_path, field_name = name.rsplit(".", 1)
        model = import_string(cls_path)
        field = model._meta.get_field(field_name)
        if isinstance(field, models.fields.related.RelatedField):
            # If a deferred attribute is a related field, it is an automatically created field
            # with the postfix "_id" and contains the reference to the id of the related model
            # instance. These are usually undocumented, so they only are included in the docs
            # is sphinx is invoked with the undoc-members option.
            lines.append(
                f"Internal field, use :class:`~{cls_path}.{field.name}` instead."
            )
        else:
            lines.extend(get_field_details(app, field))
    elif isinstance(attribute, FIELD_DESCRIPTORS):
        # Display a reasonable output for forward descriptors (foreign key and one to one fields).
        lines.extend(get_field_details(app, attribute.field))
    elif isinstance(attribute, related_descriptors.ManyToManyDescriptor):
        # Check this case first since ManyToManyDescriptor inherits from ReverseManyToOneDescriptor
        # This descriptor is used for both forward and reverse relationships
        if attribute.reverse:
            lines.extend(get_field_details(app, attribute.rel))
        else:
            lines.extend(get_field_details(app, attribute.field))
    elif isinstance(attribute, related_descriptors.ReverseManyToOneDescriptor):
        lines.extend(get_field_details(app, attribute.rel))
    elif isinstance(attribute, related_descriptors.ReverseOneToOneDescriptor):
        lines.extend(get_field_details(app, attribute.related))
    elif isinstance(attribute, (models.Manager, ManagerDescriptor)):
        # Somehow the 'objects' manager doesn't pass through the docstrings.
        module, model_name, field_name = name.rsplit(".", 2)
        lines.append("Django manager to access the ORM")
        lines.append(f"Use ``{model_name}.objects.all()`` to fetch all objects.")
    # Check if there are initial docstrings to be appended
    if docstring_lines:
        # Get default docstring of attribute
        parent_docstring = type(attribute).__doc__
        # Ignore non-string __doc__
        if not isinstance(parent_docstring, str):
            parent_docstring = ""
        # Only append the initial docstring of the attribute if it's overwritten
        if docstring_lines != prepare_docstring(parent_docstring) or not lines:
            if lines:
                # If lines are not empty, append a separating new line before docstring
                lines.append("")
            # Remove last element because it's a newline
            lines.extend(docstring_lines[:-1])


def get_field_details(app, field):
    """
    This function returns the detail docstring of a model field.
    It includes the field type and the verbose name of the field.

    :param app: The Sphinx application object
    :type app: ~sphinx.application.Sphinx

    :param field: The field
    :type field: ~django.db.models.Field

    :return: The field details as list of strings
    :rtype: list [ str ]
    """
    choices_limit = app.config.django_choices_to_show

    field_details = [
        f"Type: {get_field_type(field)}",
        "",
        f"{get_field_verbose_name(field)}",
    ]
    if hasattr(field, "choices") and field.choices:
        field_details.extend(["", "Choices:", ""])
        field_details.extend(
            [
                f"* ``{key}``" if key != "" else "* ``''`` (Empty string)"
                for key, value in field.choices[:choices_limit]
            ]
        )
        # Check if list has been truncated
        if len(field.choices) > choices_limit:
            # If only one element has been truncated, just list it as well
            if len(field.choices) == choices_limit + 1:
                field_details.append(f"* ``{field.choices[-1][0]}``")
            else:
                field_details.append(f"* and {len(field.choices) - choices_limit} more")
    return field_details
