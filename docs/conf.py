# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from sphinxcontrib_django import __version__

# -- Project information -----------------------------------------------------

project = "sphinxcontrib-django"
copyright = "2021"
author = "Timo Ludwig"

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx_last_updated_by_git",
    "sphinxcontrib_django.roles",
]

# Warn about all references where the target cannot be found
nitpicky = True

# A list of (type, target) tuples that should be ignored when :attr:`nitpicky` is ``True``
nitpick_ignore = [("py:class", "sphinx.ext.autodoc.Options")]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "sphinx_rtd_theme"
# The logos shown in the menu bar
html_logo = "images/django-sphinx-logo-white.png"
# The favicon of the html doc files
html_favicon = "images/favicon.svg"
# Do not include links to the documentation source (.rst files) in build
html_show_sourcelink = False
