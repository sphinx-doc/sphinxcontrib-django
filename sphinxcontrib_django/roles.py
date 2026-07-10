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

Additionally, this module adds the ``:py:model:`` role to cross-reference Django models by
their ``app_label.ModelName`` notation known from :mod:`django.contrib.admindocs`, e.g.
``:py:model:`auth.User``` links to the documentation of :class:`django.contrib.auth.models.User`
if the model class is documented. Full import paths are supported as well.

This module can also be used separately in ``conf.py``::

    extensions = [
        "sphinxcontrib_django.roles",
    ]
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.apps import apps
from sphinx.domains.python import PyXRefRole
from sphinx.errors import ExtensionError

from . import __version__

if TYPE_CHECKING:
    import docutils
    import sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class ModelRole(PyXRefRole):
    """
    Cross-reference role for Django models, registered as ``:py:model:``.

    In addition to the full import path accepted by ``:py:class:``, it resolves the
    ``app_label.ModelName`` notation of :mod:`django.contrib.admindocs` via the app registry,
    so the same docstrings work in both the Django admin documentation and Sphinx.
    """

    def process_link(
        self,
        env: sphinx.environment.BuildEnvironment,
        refnode: docutils.nodes.Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        """Resolve the Django model label to the full python path of the model class."""
        # Resolve the reference like a regular class cross-reference
        refnode["reftype"] = "class"
        title, target = super().process_link(
            env, refnode, has_explicit_title, title, target
        )
        if target.count(".") == 1:
            try:
                model = apps.get_model(target)
            except LookupError as e:
                logger.warning(
                    "Unable to resolve Django model reference %r: %s", target, e
                )
            else:
                target = f"{model.__module__}.{model.__qualname__}"
        return title, target


def setup(app: sphinx.application.Sphinx) -> ExtensionMetadata:
    """
    Allow this module to be used as Sphinx extension.

    This is also called from the top-level :meth:`~sphinxcontrib_django.setup`.

    It adds cross-reference types via :meth:`~sphinx.application.Sphinx.add_crossref_type` and
    the :class:`ModelRole` via :meth:`~sphinx.application.Sphinx.add_role_to_domain`.

    :param app: The Sphinx application object
    """
    # Load sphinx.ext.intersphinx extension
    app.setup_extension("sphinx.ext.intersphinx")

    # Add default intersphinx mappings after config is initialized
    app.connect("config-inited", add_default_intersphinx_mappings)

    # Allow intersphinx mappings to custom Django roles
    django_crossref_types = [
        "setting",
        "templatetag",
        "templatefilter",
        "fieldlookup",
        "django-admin",
    ]
    # Allow intersphinx mappings to custom Sphinx roles
    sphinx_crossref_types = ["event", "confval"]

    for crossref_type in django_crossref_types + sphinx_crossref_types:
        try:
            app.add_crossref_type(directivename=crossref_type, rolename=crossref_type)
        except ExtensionError as e:
            logger.warning("Unable to register cross-reference type: %s", e)

    try:
        app.add_role_to_domain("py", "model", ModelRole())
    except ExtensionError as e:
        logger.warning("Unable to register :py:model: role: %s", e)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def add_default_intersphinx_mappings(
    app: sphinx.application.Sphinx, config: sphinx.config.Config
) -> None:
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
        config.intersphinx_mapping = DEFAULT_INTERSPHINX_MAPPING
