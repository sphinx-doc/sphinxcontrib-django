from django.db import models
from django.db.models.fields import related_descriptors
from django.db.models.fields.files import FileDescriptor
from django.db.models.manager import ManagerDescriptor
from django.db.models.query_utils import DeferredAttribute
from django.utils.module_loading import import_string

_FIELD_DESCRIPTORS = (FileDescriptor,)


# Support for some common third party fields
try:
    from phonenumber_field.modelfields import PhoneNumberDescriptor

    _FIELD_DESCRIPTORS += (PhoneNumberDescriptor,)
except ImportError:
    PhoneNumberDescriptor = None


def _improve_attribute_docs(obj, name, lines):
    """Improve the documentation of various attributes.

    This improves the navigation between related objects.

    :param obj: the instance of the object to document.
    :param name: full dotted path to the object.
    :param lines: expected documentation lines.
    """
    if isinstance(obj, DeferredAttribute):
        # This only points to a field name, not a field.
        # Get the field by importing the name.
        cls_path, field_name = name.rsplit(".", 1)
        model = import_string(cls_path)
        field = model._meta.get_field(field_name)

        del lines[:]  # lines.clear() is Python 3 only
        lines.append("**Model field:** {label}".format(label=field.verbose_name))
    elif isinstance(obj, _FIELD_DESCRIPTORS):
        # These
        del lines[:]
        lines.append("**Model field:** {label}".format(label=obj.field.verbose_name))

        if isinstance(obj, FileDescriptor):
            lines.append(
                "**Return type:** :class:`~django.db.models.fields.files.FieldFile`"
            )
        elif PhoneNumberDescriptor is not None and isinstance(
            obj, PhoneNumberDescriptor
        ):
            lines.append(
                "**Return type:** :class:`~phonenumber_field.phonenumber.PhoneNumber`"
            )
    elif isinstance(obj, related_descriptors.ForwardManyToOneDescriptor):
        # Display a reasonable output for forward descriptors.
        related_model = obj.field.remote_field.model
        if isinstance(related_model, str):
            cls_path = related_model
        else:
            cls_path = "{}.{}".format(related_model.__module__, related_model.__name__)
        del lines[:]
        lines.append(
            "**Model field:** {label}, "
            "accesses the :class:`~{cls_path}` model.".format(
                label=obj.field.verbose_name, cls_path=cls_path
            )
        )
    elif isinstance(obj, related_descriptors.ReverseOneToOneDescriptor):
        related_model = obj.related.related_model
        cls_path = "{}.{}".format(related_model.__module__, related_model.__name__)
        del lines[:]
        lines.append(
            "**Model field:** {label}, "
            "accesses the :class:`~{cls_path}` model.".format(
                label=obj.related.field.verbose_name, cls_path=cls_path
            )
        )
    elif isinstance(obj, related_descriptors.ReverseManyToOneDescriptor):
        related_model = obj.rel.related_model
        cls_path = "{}.{}".format(related_model.__module__, related_model.__name__)
        del lines[:]
        lines.append(
            "**Model field:** {label}, "
            "accesses the M2M :class:`~{cls_path}` model.".format(
                label=obj.field.verbose_name, cls_path=cls_path
            )
        )
    elif isinstance(obj, (models.Manager, ManagerDescriptor)):
        # Somehow the 'objects' manager doesn't pass through the docstrings.
        module, cls_name, field_name = name.rsplit(".", 2)
        lines.append("Django manager to access the ORM")
        tpl = "Use ``{cls_name}.objects.all()`` to fetch all objects."
        lines.append(tpl.format(cls_name=cls_name))
