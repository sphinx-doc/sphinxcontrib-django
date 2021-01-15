import os
import sys

# Add directory containing dummy app to sys.path
sys.path.insert(0, os.path.abspath("."))

project = "sphinx dummy Test"
extensions = ["sphinxcontrib_django2"]

# Configure Django settings module
django_settings = "dummy_django_app.settings"

nitpicky = True
