from __future__ import annotations

import re
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
    assert len(setup_records) == 2
    assert all(record.name == "sphinxcontrib_django.roles" for record in setup_records)
    assert "Unable to register cross-reference type: " in setup_records[0].msg
    assert "Unable to register :py:model: role: " in setup_records[1].msg


@pytest.mark.sphinx("html", testroot="docstrings")
def test_model_role(app: SphinxTestApp) -> None:
    app.build()
    html = (app.outdir / "index.html").read_text(encoding="utf-8")
    links = re.findall(
        r'<a class="reference internal"'
        r' href="models\.html#dummy_django_app\.models\.SimpleModel"[^>]*>.*?</a>',
        html,
    )
    assert any("dummy_django_app.SimpleModel</span>" in link for link in links)
    assert any("dummy_django_app.models.SimpleModel</span>" in link for link in links)


@pytest.mark.sphinx("html", testroot="docstrings", freshenv=True)
def test_model_role_unknown_model(
    app: SphinxTestApp, caplog: pytest.LogCaptureFixture
) -> None:
    app.build()
    warnings = [
        record.getMessage()
        for record in caplog.records
        if record.name == "sphinxcontrib_django.roles"
    ]
    assert any("unknown_app.UnknownModel" in message for message in warnings)
