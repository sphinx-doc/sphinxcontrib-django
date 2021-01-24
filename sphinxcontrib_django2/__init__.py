"""
This is a sphinx extension which improves the documentation of Django apps.
"""
__version__ = "1.0"

from . import docstrings, roles


def setup(app):
    """
    Allow this module to be used as sphinx extension.

    Setup the two sub-extensions :mod:`~sphinxcontrib_django2.docstrings` and
    :mod:`~sphinxcontrib_django2.roles` which can also be imported separately.

    :param app: The Sphinx application object
    :type app: ~sphinx.application.Sphinx
    """
    docstrings.setup(app)
    roles.setup(app)

    return {
        "version:": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
