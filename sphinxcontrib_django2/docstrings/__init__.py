"""Improve the Django model docstrings.

For example:
* Automatically mention all model fields as parameters in the model construction.
* Mention form fields.
* Improve field representations in the documentation.

Based on:

* https://gist.github.com/abulka/48b54ea4cbc7eb014308
* https://gist.github.com/codingjoe/314bda5a07ff3b41f247
"""
from .. import config
from .attributes import _improve_attribute_docs
from .classes import _improve_class_docs
from .methods import _improve_method_docs


def setup(app):
    """Allow this package to be used as Sphinx extension.

    This is also called from the top-level ``__init__.py``.

    :type app: sphinx.application.Sphinx
    """
    from .patches import patch_django_for_autodoc

    # When running, make sure Django doesn't execute querysets
    # Fix module paths for intersphinx mappings
    patch_django_for_autodoc()

    # Generate docstrings for Django model fields
    # Register the docstring processor with sphinx
    app.connect("autodoc-process-docstring", improve_model_docstring)

    # influence skip rules
    app.connect("autodoc-skip-member", autodoc_skip)


def autodoc_skip(app, what, name, obj, skip, options):
    """Hook to tell autodoc to include or exclude certain fields.

    Sadly, it doesn't give a reference to the parent object,
    so only the ``name`` can be used for referencing.

    :type app: sphinx.application.Sphinx
    :param what: The parent type, ``class`` or ``module``
    :type what: str
    :param name: The name of the child method/attribute.
    :type name: str
    :param obj: The child value (e.g. a method, dict, or module reference)
    :param options: The current autodoc settings.
    :type options: dict

    .. seealso:: http://www.sphinx-doc.org/en/stable/ext/autodoc.html#event-autodoc-skip-member
    """
    if name in config.EXCLUDE_MEMBERS:
        return True

    if name in config.INCLUDE_MEMBERS:
        return False

    return skip


def improve_model_docstring(app, what, name, obj, options, lines):
    """Hook to improve the autodoc docstrings for Django models.

    :type app: sphinx.application.Sphinx
    :param what: The parent type, ``class`` or ``module``
    :type what: str
    :param name: The dotted path to the child method/attribute.
    :type name: str
    :param obj: The Python object that i s being documented.
    :param options: The current autodoc settings.
    :type options: dict
    :param lines: The current documentation lines
    :type lines: list
    """
    if what == "class":
        _improve_class_docs(app, obj, lines)
    elif what == "attribute":
        _improve_attribute_docs(obj, name, lines)
    elif what == "method":
        _improve_method_docs(obj, name, lines)

    # Return the extended docstring
    return lines
