from django import test
from django.db import models
from django.forms import fields, forms
from django.forms import models as form_models
from django.forms import widgets

try:
    from django.contrib.postgres.forms import array, jsonb

    POSTGRES = True
except ModuleNotFoundError:
    # In case postgres is not used, pass
    POSTGRES = False


def patch_django_for_autodoc():
    """Fix the appearance of some classes in autodoc.

    This avoids query evaluation.
    """
    # Fix Django's manager appearance
    models.manager.ManagerDescriptor.__get__ = (
        lambda self, *args, **kwargs: self.manager
    )

    # Stop Django from executing DB queries
    models.QuerySet.__repr__ = lambda self: self.__class__.__name__

    # Module paths which are documented in the parent module
    DJANGO_MODULE_PATHS = {
        "django.db.models": [models.base, models.fields],
        "django.forms": [
            forms,
            fields,
            form_models,
            widgets,
        ],
        "django.test": [test],
    }

    # Support postgres fields if used
    if POSTGRES:
        DJANGO_MODULE_PATHS["django.contrib.postgres.forms"] = [
            array,
            jsonb,
        ]
        array.__all__ = (
            "SimpleArrayField",
            "SplitArrayField",
        )
        jsonb.__all__ = ("JSONString", "JSONField")

    # Add __all__ where missing
    models.base.__all__ = ("Model", "FilteredRelation")

    # Set the __module__ to the parent module to make sure intersphinx mappings work as expected
    for parent_module_str, django_modules in DJANGO_MODULE_PATHS.items():
        for django_module in django_modules:
            for module_class in map(django_module.__dict__.get, django_module.__all__):
                try:
                    module_class.__module__ = parent_module_str
                except AttributeError:
                    pass
