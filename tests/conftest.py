"""
The recommended setup for testing sphinx extension is undocumented (see issue #7008:
https://github.com/sphinx-doc/sphinx/issues/7008), so this setup was created using the given code
snippets and the existing test cases for the autodoc extension.
"""
from unittest.mock import Mock

import pytest
from sphinx.ext.autodoc.directive import DocumenterBridge, process_documenter_options
from sphinx.testing.path import path
from sphinx.util.docutils import LoggingReporter

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    """
    Path to the root directory of the testing targets
    """
    return path(__file__).parent.abspath() / "roots"


@pytest.fixture(scope="function")
def do_autodoc():
    """
    This function simulates the autodoc functionality.

    Taken from https://github.com/sphinx-doc/sphinx/blob/d635d94eebbca0ebb1a5402aa07ed58c0464c6d3/tests/test_ext_autodoc.py#L33-L45 # noqa: E501
    """

    def do_autodoc(app, objtype, name, options=None):
        if options is None:
            options = {}
        app.env.temp_data.setdefault("docname", "index")  # set dummy docname
        doccls = app.registry.documenters[objtype]
        docoptions = process_documenter_options(doccls, app.config, options)
        state = Mock()
        state.document.settings.tab_width = 8
        bridge = DocumenterBridge(app.env, LoggingReporter(""), docoptions, 1, state)
        documenter = doccls(bridge, name)
        documenter.generate()
        return bridge.result

    return do_autodoc


@pytest.fixture(scope="function")
def app_with_conflicting_extension(app_params, make_app):
    """
    Simulate the usage of a conflicting extension which also registers a "setting" directive
    """
    args, kwargs = app_params
    kwargs["confoverrides"] = {
        "extensions": [
            "sphinx.ext.autodoc",
            "conflicting_sphinx_extension",
            "sphinxcontrib_django2",
        ]
    }
    app_ = make_app(*args, **kwargs)
    yield app_
