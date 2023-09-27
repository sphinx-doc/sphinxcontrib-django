"""
The recommended setup for testing sphinx extension is undocumented (see issue #7008:
https://github.com/sphinx-doc/sphinx/issues/7008), so this setup was created using the given code
snippets and the existing test cases for the autodoc extension.
"""
from __future__ import annotations

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
def app(test_params, app_params, make_app, shared_result, requests_mock):
    """
    Overwrite sphinx.testing.fixtures.app to take the additional fixture requests_mock to fake
    intersphinx requests
    """
    args, kwargs = app_params
    app_ = make_app(*args, **kwargs)
    yield app_


@pytest.fixture(scope="function")
def setup_app_with_different_config(app_params, make_app):
    """
    Simulate the setup of the sphinx app with a different config
    Return the function instead of the final app object to make sure exceptions occur inside the
    test and not inside the fixture
    """

    def setup_app_with_different_config(**confoverrides):
        args, kwargs = app_params
        kwargs["confoverrides"] = confoverrides
        return make_app(*args, **kwargs)

    return setup_app_with_different_config


@pytest.fixture(scope="function")
def do_autodoc():
    """
    This function simulates the autodoc functionality.

    Taken from https://github.com/sphinx-doc/sphinx/blob/d635d94eebbca0ebb1a5402aa07ed58c0464c6d3/tests/test_ext_autodoc.py#L33-L45
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
