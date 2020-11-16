"""Adding extra roles for documentation writing."""
import logging

from sphinx.errors import ExtensionError

logger = logging.getLogger(__name__)


def setup(app):
    """Allow this module to be used as Sphinx extension.

    This is also called from the top-level ``__init__.py``.
    It adds the rules to allow :django:setting:`SITE_ID` to work.

    :type app: sphinx.application.Sphinx
    """
    try:
        app.add_crossref_type(
            directivename="setting",
            rolename="setting",
            indextemplate="pair: %s; setting",
        )
    except ExtensionError as e:
        logger.warning("Unable to register :django:setting:`..`: " + str(e))
