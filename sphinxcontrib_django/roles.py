"""
This module adds cross-reference types which are used in the documentation of Django and Sphinx to
allow intersphinx mappings to these custom types.
The supported text roles are:

Django:

* ``:setting:``, e.g. ``:setting:`INSTALLED_APPS``` renders as :setting:`INSTALLED_APPS`
* ``:templatetag:``, e.g. ``:templatetag:`block``` renders as :templatetag:`block`
* ``:templatefilter:``, e.g. ``:templatefilter:`add``` renders as :templatefilter:`add`
* ``:fieldlookup:``, e.g. ``:fieldlookup:`equals``` renders as :fieldlookup:`equals`

Sphinx:

* ``:event:``, e.g. ``:event:`autodoc-skip-member``` renders as :event:`autodoc-skip-member`
* ``:confval:``, e.g. ``:confval:`extensions``` renders as :confval:`extensions`

This module can also be used separately in ``conf.py``::

    extensions = [
        "sphinxcontrib_django.roles",
    ]
"""
from __future__ import annotations

import logging

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.errors import ExtensionError

from . import __version__

logger = logging.getLogger(__name__)


def setup(app: Sphinx) -> dict:
    """
    Allow this module to be used as Sphinx extension.

    This is also called from the top-level :meth:`~sphinxcontrib_django.setup`.

    It adds cross-reference types via :meth:`~sphinx.application.Sphinx.add_crossref_type`.

    :param app: The Sphinx application object
    """
    # Load sphinx.ext.intersphinx extension
    app.setup_extension("sphinx.ext.intersphinx")

    # Add default intersphinx mappings after config is initialized
    app.connect("config-inited", add_default_intersphinx_mappings)

    # Allow intersphinx mappings to custom Django roles
    django_crossref_types = ["setting", "templatetag", "templatefilter", "fieldlookup"]
    # Allow intersphinx mappings to custom Sphinx roles
    sphinx_crossref_types = ["event", "confval"]

    for crossref_type in django_crossref_types + sphinx_crossref_types:
        try:
            app.add_crossref_type(directivename=crossref_type, rolename=crossref_type)
        except ExtensionError as e:
            logger.warning("Unable to register cross-reference type: %s", e)

    return {
        "version:": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def add_default_intersphinx_mappings(app: Sphinx, config: Config) -> None:
    """
    This function provides a default intersphinx mapping to the documentations of Python, Django
    and Sphinx if ``intersphinx_mapping`` is not given in ``conf.py``.

    Called on the :event:`config-inited` event.

    :param app: The Sphinx application object
    :param config: The Sphinx configuration
    """
    DEFAULT_INTERSPHINX_MAPPING = {
        "python": ("https://docs.python.org/", None),
        "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
        "django": (
            "https://docs.djangoproject.com/en/stable/",
            "https://docs.djangoproject.com/en/stable/_objects/",
        ),
    }
    if not config.intersphinx_mapping:
        # TYPING: type hints are missing `.intersphinx_mapping` attribute.
        config.intersphinx_mapping = DEFAULT_INTERSPHINX_MAPPING  # type: ignore[attr-defined ]
