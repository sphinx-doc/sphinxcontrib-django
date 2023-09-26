"""
This is a sphinx extension which improves the documentation of Django apps.
"""

from __future__ import annotations

__version__ = "2.5"

from sphinx.application import Sphinx

from . import docstrings, roles


def setup(app: Sphinx) -> dict:
    """
    Allow this module to be used as sphinx extension.

    Setup the two sub-extensions :mod:`~sphinxcontrib_django.docstrings` and
    :mod:`~sphinxcontrib_django.roles` which can also be imported separately.

    :param app: The Sphinx application object
    """
    docstrings.setup(app)
    roles.setup(app)

    return {
        "version:": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
