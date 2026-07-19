from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sphinx.errors import ConfigError

if TYPE_CHECKING:
    from collections.abc import Callable

    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="docstrings")
def test_setup_with_missing_config(
    setup_app_with_different_config: Callable[..., SphinxTestApp],
) -> None:
    """
    Simulate the missing configuration of the Django settings
    """
    with pytest.raises(ConfigError):
        setup_app_with_different_config(django_settings="")


@pytest.mark.sphinx("html", testroot="docstrings")
def test_setup_with_incorrect_config(
    setup_app_with_different_config: Callable[..., SphinxTestApp],
) -> None:
    """
    Simulate the incorrect configuration of the Django settings
    """
    with pytest.raises(ConfigError):
        setup_app_with_different_config(django_settings="non_existing_module.settings")
