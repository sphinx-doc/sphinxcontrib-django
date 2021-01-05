"""
This module contains patches for Django to improve its interaction with Sphinx.
"""
from django import forms, test
from django.db import models

try:
    from django.contrib.postgres import fields as postgres_fields
    from django.contrib.postgres import forms as postgres_forms

    POSTGRES = True
except ModuleNotFoundError:
    # In case postgres is not used, pass
    POSTGRES = False


def patch_django_for_autodoc():
    """
    Fix the appearance of some classes in autodoc.
    E.g. the absolute path to the base model class is ``django.db.models.base.Model``, but its
    intersphinx mapping path is ``django.db.models.Model``.

    This also avoids query evaluation.
    """
    # Fix Django's manager appearance
    models.manager.ManagerDescriptor.__get__ = (
        lambda self, *args, **kwargs: self.manager
    )

    # Stop Django from executing DB queries
    models.QuerySet.__repr__ = lambda self: self.__class__.__name__

    # Module paths which are documented in the parent module
    DJANGO_MODULE_PATHS = {
        "django.db.models": [
            models.base,
            models.fields,
            models.fields.files,
            models.fields.related,
        ],
        "django.forms": [
            forms.forms,
            forms.fields,
            forms.models,
            forms.widgets,
        ],
        "django.test": [test],
    }

    # Support postgres fields if used
    if POSTGRES:
        DJANGO_MODULE_PATHS["django.contrib.postgres.forms"] = [
            postgres_forms.array,
            postgres_forms.jsonb,
        ]
        DJANGO_MODULE_PATHS["django.contrib.postgres.fields"] = [
            postgres_fields.array,
            postgres_fields.jsonb,
        ]
        postgres_forms.array.__all__ = (
            "SimpleArrayField",
            "SplitArrayField",
        )
        postgres_forms.jsonb.__all__ = ("JSONString", "JSONField")

    # Add __all__ where missing
    models.base.__all__ = ("Model", "FilteredRelation")
    models.fields.files.__all__ = ("FileField", "ImageField")
    models.fields.related.__all__ = ("ForeignKey", "OneToOneField", "ManyToManyField")

    # Set the __module__ to the parent module to make sure intersphinx mappings work as expected
    for parent_module_str, django_modules in DJANGO_MODULE_PATHS.items():
        for django_module in django_modules:
            for module_class in map(django_module.__dict__.get, django_module.__all__):
                try:
                    module_class.__module__ = parent_module_str
                except AttributeError:
                    pass
