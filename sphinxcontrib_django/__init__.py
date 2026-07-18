"""
This is a sphinx extension which improves the documentation of Django apps.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

try:
    __version__ = version("sphinxcontrib-django")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0.dev0"

from . import docstrings, roles

if TYPE_CHECKING:
    import sphinx
    from sphinx.util.typing import ExtensionMetadata


def setup(app: sphinx.application.Sphinx) -> ExtensionMetadata:
    """
    Allow this module to be used as sphinx extension.

    Setup the two sub-extensions :mod:`~sphinxcontrib_django.docstrings` and
    :mod:`~sphinxcontrib_django.roles` which can also be imported separately.

    :param app: The Sphinx application object
    """
    docstrings.setup(app)
    roles.setup(app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
