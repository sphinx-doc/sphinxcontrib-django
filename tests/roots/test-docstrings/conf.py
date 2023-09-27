from __future__ import annotations

import os
import sys

# Add directory containing dummy app to sys.path
sys.path.insert(0, os.path.abspath("."))

project = "sphinx dummy Test"
extensions = [
    "sphinxcontrib_django",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
]

# Configure Django settings module
django_settings = "dummy_django_app.settings"

nitpicky = True


def patch_django_for_autodoc(app):
    """
    Monkeypatch application
    """
    from dummy_django_app.models import MonkeyPatched

    MonkeyPatched.__doc__ = "Monkeypatched docstring"


def setup(app):
    # Run method after Django config is initialized
    app.connect("django-configured", patch_django_for_autodoc)
