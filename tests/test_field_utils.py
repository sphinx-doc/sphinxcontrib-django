import copy

import pytest

from sphinxcontrib_django.docstrings.field_utils import get_field_verbose_name


@pytest.mark.sphinx("html", testroot="docstrings")
def test_reverse_rel_with_lazy_reference(app):
    # Simulate an unresolved lazy reference (see issue #43)
    from dummy_django_app2.models import GenericRelationModel

    field = copy.copy(
        GenericRelationModel._meta.get_field("relation_field").remote_field
    )
    field.model = "dummy_django_app.TaggedItem"
    assert get_field_verbose_name(field) == (
        "All generic relation models of this tagged item (related name of"
        " :attr:`~dummy_django_app2.models.GenericRelationModel.relation_field`)"
    )


@pytest.mark.sphinx("html", testroot="docstrings")
def test_one_to_one_rel_with_lazy_reference(app):
    from dummy_django_app.models import SimpleModel

    field = copy.copy(SimpleModel._meta.get_field("childA").remote_field)
    field.model = "dummy_django_app.ChildModelA"
    assert get_field_verbose_name(field) == (
        "The simple model of this child model a (related name of"
        " :attr:`~dummy_django_app.models.SimpleModel.childA`)"
    )


@pytest.mark.sphinx("html", testroot="docstrings")
def test_hidden_related_name_is_not_rendered(app):
    # related_name="+" disables the reverse accessor, so the literal "+" must
    # not appear in the docs
    from dummy_django_app2.models import GenericRelationModel

    field = GenericRelationModel._meta.get_field("relation_field").remote_field
    assert get_field_verbose_name(field) == (
        "All generic relation models of this tagged item (related name of"
        " :attr:`~dummy_django_app2.models.GenericRelationModel.relation_field`)"
    )
