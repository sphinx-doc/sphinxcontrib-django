from __future__ import annotations

from sphinx.domains.python import PyXRefRole


def setup(app):
    """
    Sphinx extension which also registers a "setting" directive and a "py:model" role
    """
    app.add_crossref_type(
        directivename="setting", rolename="setting", indextemplate="pair: %s; setting"
    )
    app.add_role_to_domain("py", "model", PyXRefRole())
