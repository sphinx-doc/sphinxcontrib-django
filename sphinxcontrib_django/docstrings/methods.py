"""
This module contains all functions which are used to improve the documentation of methods.
"""
import re

RE_GET_FOO_DISPLAY = re.compile(r"\.get_(?P<field>[a-zA-Z0-9_]+)_display$")
RE_GET_NEXT_BY = re.compile(r"\.get_next_by_(?P<field>[a-zA-Z0-9_]+)$")
RE_GET_PREVIOUS_BY = re.compile(r"\.get_previous_by_(?P<field>[a-zA-Z0-9_]+)$")


def improve_method_docstring(name, lines):
    """
    Improve the documentation of methods automatically contributed to models by Django:

    * :meth:`~django.db.models.Model.get_FOO_display`
    * :meth:`~django.db.models.Model.get_next_by_FOO`
    * :meth:`~django.db.models.Model.get_previous_by_FOO`

    :param name: The full dotted path to the object.
    :type name: str

    :param lines: The lines of docstring lines
    :type lines: list [ str ]
    """
    if not lines:
        # Not doing obj.__module__ lookups to avoid performance issues.
        if name.endswith("_display"):
            match = RE_GET_FOO_DISPLAY.search(name)
            if match is not None:
                # Django get_..._display method
                lines.append(
                    f"Shows the label of the :attr:`{match.group('field')}`. See"
                    " :meth:`~django.db.models.Model.get_FOO_display` for more"
                    " information."
                )
        elif ".get_next_by_" in name:
            match = RE_GET_NEXT_BY.search(name)
            if match is not None:
                lines.append(
                    f"Finds next instance based on :attr:`{match.group('field')}`. See"
                    " :meth:`~django.db.models.Model.get_next_by_FOO` for more"
                    " information."
                )
        elif ".get_previous_by_" in name:
            match = RE_GET_PREVIOUS_BY.search(name)
            if match is not None:
                lines.append(
                    f"Finds previous instance based on :attr:`{match.group('field')}`."
                    " See :meth:`~django.db.models.Model.get_previous_by_FOO` for more"
                    " information."
                )
