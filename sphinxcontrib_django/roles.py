"""Adding extra roles for documentation writing."""


def setup(app):
    """Allow this module to be used as Sphinx extension.
    This is also called from the top-level ``__init__.py``.

    It adds the rules to allow :django:setting:`SITE_ID` to work.

    :type app: sphinx.application.Sphinx
    """
    app.add_crossref_type(
        directivename="setting",
        rolename="setting",
        indextemplate="pair: %s; setting",
    )
