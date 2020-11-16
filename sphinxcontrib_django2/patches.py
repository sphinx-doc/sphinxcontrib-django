from django.db import models
from django.db.models.manager import ManagerDescriptor


def patch_django_for_autodoc():
    """Fix the appearance of some classes in autodoc.

    This avoids query evaluation.
    """
    # Fix Django's manager appearance
    ManagerDescriptor.__get__ = lambda self, *args, **kwargs: self.manager

    # Stop Django from executing DB queries
    models.QuerySet.__repr__ = lambda self: self.__class__.__name__
