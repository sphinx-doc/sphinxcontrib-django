from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from docutils.statemachine import StringList
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="docstrings")
def test_exclude_members(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    options = {"members": None, "undoc-members": None}
    assert not any(
        "base_fields" in line
        for line in do_autodoc(app, "module", "dummy_django_app.forms", options)
    )


@pytest.mark.sphinx("html", testroot="docstrings")
def test_include_members(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    options = {"members": None}
    assert any(
        "__init__" in line
        for line in do_autodoc(app, "module", "dummy_django_app.forms", options)
    )
