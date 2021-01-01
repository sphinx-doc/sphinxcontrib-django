from django import forms
from django.apps import apps
from django.db import models
from django.utils.encoding import force_str
from django.utils.html import strip_tags


def _improve_class_docs(app, cls, lines):
    """Improve the documentation of a class."""
    if issubclass(cls, models.Model):
        _add_model_fields_as_params(app, cls, lines)
    elif issubclass(cls, forms.BaseForm):
        _add_form_fields(cls, lines)


def _add_model_fields_as_params(app, obj, lines):
    """Improve the documentation of a Django model subclass.

    This adds all model fields as parameters to the ``__init__()`` method.

    :type app: sphinx.application.Sphinx
    :type lines: list
    """
    param_offset = len(":param ")
    type_offset = len(":type ")
    predefined_params = [
        line[param_offset : line.find(":", param_offset)]
        for line in lines
        if line.startswith(":param ") and ":" in line[param_offset:]
    ]
    predefined_types = [
        line[type_offset : line.find(":", type_offset)]
        for line in lines
        if line.startswith(":type ") and ":" in line[type_offset:]
    ]

    for field in obj._meta.get_fields():
        try:
            help_text = strip_tags(force_str(field.help_text))
            verbose_name = force_str(field.verbose_name).capitalize()
        except AttributeError:
            # e.g. ManyToOneRel
            continue

        # Add parameter
        if field.name not in predefined_params:
            if help_text:
                if verbose_name:
                    if not verbose_name.strip().endswith("."):
                        verbose_name += "."
                    help_text = verbose_name + " " + help_text
                lines.append(u":param %s: %s" % (field.name, help_text))
            else:
                lines.append(u":param %s: %s" % (field.name, verbose_name))

        # Add type
        if field.name not in predefined_types:
            lines.append(_get_field_type(field))

    if (
        "sphinx.ext.inheritance_diagram" in app.extensions
        and "sphinx.ext.graphviz" in app.extensions
        and not any("inheritance-diagram::" in line for line in lines)
    ):
        lines.append(".. inheritance-diagram::")  # pragma: no cover


def _get_field_type(field):
    if isinstance(field, models.ForeignKey):
        to = field.remote_field.model
        if isinstance(to, str):
            to = _resolve_model(field, to)

        return u":type %s: %s to :class:`~%s.%s`" % (
            field.name,
            type(field).__name__,
            to.__module__,
            to.__name__,
        )
    else:
        return u":type %s: %s" % (field.name, type(field).__name__)


def _resolve_model(field, to):
    if "." in to:
        return apps.get_model(to)
    elif to == "self":
        return field.model
    else:
        return apps.get_model(field.model._meta.app_label, to)


def _add_form_fields(obj, lines):
    """Improve the documentation of a Django Form class.

    This highlights the available fields in the form.
    """
    lines.append("**Form fields:**")
    lines.append("")
    for name, field in obj.base_fields.items():
        field_type = "{}.{}".format(
            field.__class__.__module__, field.__class__.__name__
        )
        tpl = "* ``{name}``: {label} (:class:`~{field_type}`)"
        lines.append(
            tpl.format(
                name=name,
                field=field,
                label=field.label or name.replace("_", " ").title(),
                field_type=field_type,
            )
        )
