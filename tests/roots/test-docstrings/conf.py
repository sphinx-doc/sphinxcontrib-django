import os
import sys

import django

sys.path.insert(0, os.path.abspath("."))

os.environ["DJANGO_SETTINGS_MODULE"] = "dummy_django_app.settings"

# Setup Django
django.setup()

project = "sphinx dummy Test"
extensions = ["sphinxcontrib_django2"]

nitpicky = True
