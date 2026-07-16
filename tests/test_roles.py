from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    "html",
    testroot="docstrings",
    confoverrides={
        "extensions": ["conflicting_sphinx_extension", "sphinxcontrib_django"]
    },
)
def test_setup_with_conflicting_extension(
    app: SphinxTestApp, caplog: pytest.LogCaptureFixture
) -> None:
    setup_records = caplog.get_records("setup")
    assert len(setup_records) == 1
    assert setup_records[0].name == "sphinxcontrib_django.roles"
    assert "Unable to register cross-reference type: " in setup_records[0].msg
