from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.conf import settings
from django.db.models import AutoField

if TYPE_CHECKING:
    from collections.abc import Callable

    from docutils.statemachine import StringList
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="docstrings")
def test_django_configured(
    app: SphinxTestApp, do_autodoc: Callable[..., StringList]
) -> None:
    actual = do_autodoc(app, "class", "dummy_django_app.models.MonkeyPatched")
    print(actual)
    autofield = getattr(
        settings,
        "DEFAULT_AUTO_FIELD",
        f"{AutoField.__module__}.{AutoField.__qualname__}",
    )
    assert list(actual) == [
        "",
        ".. py:class:: MonkeyPatched(*args, **kwargs)",
        "   :module: dummy_django_app.models",
        "",
        "   Monkeypatched docstring",
        "",
        "   :param id: Primary key: ID",
        f"   :type id: ~{autofield}",
        "",
        "   .. inheritance-diagram:: dummy_django_app.models.MonkeyPatched",
        "",
    ]
