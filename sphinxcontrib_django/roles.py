"""Adding extra roles for documentation writing."""
import logging

from django.apps import apps
from sphinx.domains.python import PyXRefRole
from sphinx.errors import ExtensionError

logger = logging.getLogger(__name__)


class ModelRole(PyXRefRole):
    """Expose Django models as roles for Sphinx."""

    def process_link(self, env, refnode, has_explicit_title, title, target):
        """Get full python path to model."""
        model = apps.get_model(target)
        target = ".".join([model.__module__, model.__qualname__])

        return super().process_link(
            env, refnode, has_explicit_title, title, target
        )


def setup(app):
    """Allow this module to be used as Sphinx extension.

    This is also called from the top-level ``__init__.py``.
    It adds the rules to allow :django:setting:`SITE_ID` and
    :py:model:`app.Model` to work.

    :type app: sphinx.application.Sphinx
    """
    try:
        app.add_crossref_type(
            directivename="setting",
            rolename="setting",
            indextemplate="pair: %s; setting",
        )
    except ExtensionError as e:
        logger.warning("Unable to register :django:setting:`..`: %(e)s", {e: str(e)})

    try:
        app.add_role_to_domain("py", "class", ModelRole())
    except ExtensionError as e:
        logger.warning("Unable to register :py:model:`..`: %(e)s", {e: str(e)})
