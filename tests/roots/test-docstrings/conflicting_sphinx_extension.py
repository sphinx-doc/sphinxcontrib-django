def setup(app):
    """
    Sphinx extension which also registers a "setting" directive
    """
    app.add_crossref_type(
        directivename="setting",
        rolename="setting",
        indextemplate="pair: %s; setting",
    )
