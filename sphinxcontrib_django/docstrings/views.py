"""
This module contains all functions which are used to improve the documentation of views.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django import conf
from django.urls import get_resolver

if TYPE_CHECKING:
    from collections.abc import Callable


def improve_view_docstring(obj: Callable, lines: list[str]) -> None:
    """
    Add the URL paths under which a view function is reachable to its docstring.

    Functions which are not mapped to any URL are left unchanged.

    :param obj: The documented view function
    :param lines: The docstring lines of the documented view
    """
    if not getattr(conf.settings, "ROOT_URLCONF", None):
        return

    url_paths = [
        pattern % {param: f"<{param}>" for param in params}
        for possibilities, *_ in get_resolver().reverse_dict.getlist(obj)
        for pattern, params in possibilities
    ]

    if url_paths:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(["URL paths:", ""])
        lines.extend(f"* ``/{url_path}``" for url_path in sorted(url_paths))
