import os

import django
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.test import SimpleTestCase
from django.utils.module_loading import import_string
from sphinx.application import Sphinx

try:
    from phonenumber_field.modelfields import PhoneNumberField

    PHONENUMBER = True
except ModuleNotFoundError:
    # In case phonenumber is not used, pass
    PHONENUMBER = False

import sphinxcontrib_django2
from sphinxcontrib_django2 import docstrings


class User2(models.Model):
    pass


class SimpleModel(models.Model):
    user = models.ForeignKey(
        User,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="This should help you",
        verbose_name="Very verbose name of user field",
    )
    user2 = models.ForeignKey("User2", related_name="+", on_delete=models.CASCADE)
    user3 = models.ForeignKey("auth.User", related_name="+", on_delete=models.CASCADE)
    dummy_field = models.CharField(max_length=3)

    # Mock get_..._display methods of Django models
    def get_dummy_field_display(self):
        """pass"""

    def get_next_by_dummy_field(self):
        """pass"""

    def get_previous_by_dummy_field(self):
        """pass"""


class FileModel(models.Model):
    file = models.FileField()


if PHONENUMBER:

    class PhoneNumberModel(models.Model):
        phone_number = PhoneNumberField()


class SimpleModel2(models.Model):
    simple_model = models.ForeignKey(
        SimpleModel, related_name="simple_model2", on_delete=models.CASCADE
    )
    file = models.OneToOneField(
        FileModel,
        related_name="simple_model2",
        on_delete=models.CASCADE,
    )


class SimpleForm(forms.ModelForm):
    test1 = forms.CharField(label="Test1")
    test2 = forms.CharField(help_text="Test2")

    class Meta:
        model = SimpleModel
        fields = ("user", "user2", "user3")


class TestDocStrings(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDocStrings, cls).setUpClass()
        root = os.path.dirname(sphinxcontrib_django2.__file__)
        confdir = os.path.join(os.path.dirname(__file__), "testdocs")
        cls.app = Sphinx(
            srcdir=root,
            confdir=confdir,
            outdir=os.path.join(confdir, "_build"),
            doctreedir=root,
            buildername="html",
            freshenv=True,
        )
        sphinxcontrib_django2.setup(cls.app)

    def test_foreignkey_type(self):
        """Test how the foreignkeys are rendered."""
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user")),
            ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`",
        )
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user2")),
            ":type user2: ForeignKey to"
            " :class:`~sphinxcontrib_django2.tests.test_docstrings.User2`",
        )
        self.assertEqual(
            docstrings._get_field_type(SimpleModel._meta.get_field("user3")),
            ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`",
        )

    def test_model_init_params(self):
        """Model __init__ gets all fields as params."""
        lines = []
        name = "{}.{}".format(SimpleModel.__module__, SimpleModel.__name__)
        docstrings.improve_model_docstring(
            self.app, "class", name, SimpleModel, {}, lines
        )
        self.assertEqual(
            lines,
            [
                ":param id: Id",
                ":type id: AutoField",
                ":param user: Very verbose name of user field. This should help you",
                ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`",
                ":param user2: User2",
                ":type user2: ForeignKey to"
                " :class:`~sphinxcontrib_django2.tests.test_docstrings.User2`",
                ":param user3: User3",
                ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`",
                ":param dummy_field: Dummy field",
                ":type dummy_field: CharField",
            ],
        )

    def test_add_form_fields(self):
        """Form fields should be mentioned."""
        lines = []
        name = "{}.{}".format(SimpleForm.__module__, SimpleForm.__name__)
        docstrings.improve_model_docstring(
            self.app, "class", name, SimpleForm, {}, lines
        )
        self.assertEqual(
            lines,
            [
                "**Form fields:**",
                "",
                "* ``user``: Very verbose name of user field"
                " (:class:`~django.forms.ModelChoiceField`)",
                "* ``user2``: User2 (:class:`~django.forms.ModelChoiceField`)",
                "* ``user3``: User3 (:class:`~django.forms.ModelChoiceField`)",
                "* ``test1``: Test1 (:class:`~django.forms.CharField`)",
                "* ``test2``: Test2 (:class:`~django.forms.CharField`)",
            ],
        )

    def test_deferred_model_fields(self):
        lines = []
        simple_model_path = "{}.{}".format(SimpleModel.__module__, SimpleModel.__name__)
        if django.VERSION < (3, 0):
            obj = DeferredAttribute(field_name="dummy_field")
        else:
            model = import_string(simple_model_path)
            obj = DeferredAttribute(field=model._meta.get_field("dummy_field"))

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            "{}.dummy_field".format(simple_model_path),
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** dummy field",
            ],
        )

    def test_foreignkey_model_fields(self):
        lines = []
        name = "{}.{}.user".format(SimpleModel.__module__, SimpleModel.__name__)
        obj = SimpleModel.user

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** Very verbose name of user field, accesses the "
                ":class:`~django.contrib.auth.models.User` model.",
            ],
        )

    def test_reverse_foreignkey_model_fields(self):
        lines = []
        name = "{}.{}.simple_model2".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.simple_model2

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** simple model, accesses the M2M "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel2` model.",
            ],
        )

    def test_onetoone_model_fields(self):
        lines = []
        name = "{}.{}.file".format(SimpleModel2.__module__, SimpleModel2.__name__)
        obj = SimpleModel2.file

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** file, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.FileModel` model.",
            ],
        )

    def test_reverse_onetoone_model_fields(self):
        lines = []
        name = "{}.{}.simple_model2".format(FileModel.__module__, FileModel.__name__)
        obj = FileModel.simple_model2

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** file, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel2` model.",
            ],
        )

    def test_file_field(self):
        lines = []
        name = "{}.{}.file".format(FileModel.__module__, FileModel.__name__)
        obj = FileModel.file

        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Model field:** file",
                "**Return type:** :class:`~django.db.models.fields.files.FieldFile`",
            ],
        )

    if PHONENUMBER:

        def test_phonenumber_field(self):
            lines = []
            name = "{}.{}.phone_number".format(
                PhoneNumberModel.__module__, PhoneNumberModel.__name__
            )
            obj = PhoneNumberModel.phone_number

            docstrings.improve_model_docstring(
                self.app,
                "attribute",
                name,
                obj,
                {},
                lines,
            )
            self.assertEqual(
                lines,
                [
                    "**Model field:** phone number",
                    "**Return type:** :class:`~phonenumber_field.phonenumber.PhoneNumber`",
                ],
            )

    def test_attribute_none(self):
        lines = []
        docstrings.improve_model_docstring(
            self.app,
            "attribute",
            "None",
            None,
            {},
            lines,
        )
        self.assertEqual(lines, [])

    def test_model_method_display(self):
        lines = []
        name = "{}.{}.get_dummy_field_display".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.get_dummy_field_display

        docstrings.improve_model_docstring(
            self.app,
            "method",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Autogenerated:** Shows the label of the :attr:`dummy_field`",
            ],
        )

    def test_model_method_get_next_by(self):
        lines = []
        name = "{}.{}.get_next_by_dummy_field".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.get_next_by_dummy_field

        docstrings.improve_model_docstring(
            self.app,
            "method",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Autogenerated:** Finds next instance based on :attr:`dummy_field`.",
            ],
        )

    def test_model_method_get_previous_by(self):
        lines = []
        name = "{}.{}.get_previous_by_dummy_field".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.get_previous_by_dummy_field

        docstrings.improve_model_docstring(
            self.app,
            "method",
            name,
            obj,
            {},
            lines,
        )
        self.assertEqual(
            lines,
            [
                "**Autogenerated:** Finds previous instance based on :attr:`dummy_field`.",
            ],
        )

    def test_skip_member(self):
        obj = SimpleModel
        for skip in [True, False]:
            skipped = docstrings.autodoc_skip(
                self.app, "class", obj.__name__, obj, skip, {}
            )
            self.assertEqual(skipped, skip)

    def test_skip_member_exclude(self):
        obj = SimpleForm.Meta
        for skip in [True, False]:
            skipped = docstrings.autodoc_skip(
                self.app, "class", obj.__name__, obj, skip, {}
            )
            self.assertTrue(skipped)

    def test_skip_member_include(self):
        obj = SimpleForm.__init__
        for skip in [True, False]:
            skipped = docstrings.autodoc_skip(
                self.app, "class", obj.__name__, obj, skip, {}
            )
            self.assertFalse(skipped)
