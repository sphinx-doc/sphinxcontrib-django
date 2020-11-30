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


class SimpleModelManager(models.Manager):
    pass


class FileModel(models.Model):
    file = models.FileField()


class SimpleModel(models.Model):
    # Foreign Keys
    foreignkey_user = models.ForeignKey(
        User, related_name="+", on_delete=models.CASCADE
    )
    foreignkey_user_str = models.ForeignKey(
        "auth.User", related_name="+", on_delete=models.CASCADE
    )
    foreignkey_self = models.ForeignKey(
        "self", related_name="reverse_foreignkey_self", on_delete=models.CASCADE
    )

    # One to one field
    onetoonefield = models.OneToOneField(
        FileModel,
        related_name="reverse_onetoonefield",
        on_delete=models.CASCADE,
    )
    onetoonefield_str = models.OneToOneField(
        "FileModel",
        related_name="reverse_onetoonefield_str",
        on_delete=models.CASCADE,
    )

    # Dummy field
    dummy_field = models.CharField(
        max_length=3,
        help_text="This should help you",
        verbose_name="Very verbose name of dummy field",
    )

    # Custom model manager
    custom_objects = SimpleModelManager()

    # Mock get_..._display method of Django models
    def get_dummy_field_display(self):
        """pass"""

    # Mock common get_next_by_ method
    def get_next_by_dummy_field(self):
        """pass"""

    # Mock common get_previous_by_ method
    def get_previous_by_dummy_field(self):
        """pass"""


class SimpleModel2(models.Model):
    # Foreign Keys
    foreignkey_simple_model = models.ForeignKey(
        SimpleModel,
        related_name="reverse_foreignkey_simple_model",
        on_delete=models.CASCADE,
    )
    foreignkey_simple_model_str = models.ForeignKey(
        "SimpleModel",
        related_name="reverse_foreignkey_simple_model_str",
        on_delete=models.CASCADE,
    )


if PHONENUMBER:

    class PhoneNumberModel(models.Model):
        phone_number = PhoneNumberField()


class SimpleForm(forms.ModelForm):
    test1 = forms.CharField(label="Test1")
    test2 = forms.CharField(help_text="Test2")

    class Meta:
        model = SimpleModel
        fields = (
            "foreignkey_user",
            "foreignkey_user_str",
            "foreignkey_self",
            "dummy_field",
        )


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

        # Fields of SimpleModel
        field = SimpleModel._meta.get_field("foreignkey_user_str")
        field.remote_field.model = "auth.User"
        self.assertEqual(
            docstrings._get_field_type(field),
            ":type foreignkey_user_str: ForeignKey to :class:`~django.contrib.auth.models.User`",
        )
        field = SimpleModel._meta.get_field("foreignkey_self")
        field.remote_field.model = "self"
        self.assertEqual(
            docstrings._get_field_type(field),
            ":type foreignkey_self: ForeignKey to "
            ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel`",
        )

        # Fields of SimpleModel2
        field = SimpleModel2._meta.get_field("foreignkey_simple_model_str")
        field.remote_field.model = "SimpleModel"
        self.assertEqual(
            docstrings._get_field_type(field),
            ":type foreignkey_simple_model_str: ForeignKey to "
            ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel`",
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
                ":param foreignkey_user: Foreignkey user",
                ":type foreignkey_user: ForeignKey to :class:`~django.contrib.auth.models.User`",
                ":param foreignkey_user_str: Foreignkey user str",
                ":type foreignkey_user_str: ForeignKey to "
                ":class:`~django.contrib.auth.models.User`",
                ":param foreignkey_self: Foreignkey self",
                ":type foreignkey_self: ForeignKey to"
                " :class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel`",
                ":param onetoonefield: Onetoonefield",
                ":type onetoonefield: OneToOneField to "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.FileModel`",
                ":param onetoonefield_str: Onetoonefield str",
                ":type onetoonefield_str: OneToOneField to "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.FileModel`",
                ":param dummy_field: Very verbose name of dummy field. This should help you",
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
                "* ``foreignkey_user``: Foreignkey user (:class:`~django.forms.ModelChoiceField`)",
                "* ``foreignkey_user_str``: Foreignkey user str "
                "(:class:`~django.forms.ModelChoiceField`)",
                "* ``foreignkey_self``: Foreignkey self (:class:`~django.forms.ModelChoiceField`)",
                "* ``dummy_field``: Very verbose name of dummy field "
                "(:class:`~django.forms.CharField`)",
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
                "**Model field:** Very verbose name of dummy field",
            ],
        )

    def test_foreignkey_model_fields(self):
        lines = []
        name = "{}.{}.foreignkey_simple_model".format(
            SimpleModel2.__module__, SimpleModel2.__name__
        )
        obj = SimpleModel2.foreignkey_simple_model

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
                "**Model field:** foreignkey simple model, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel` model.",
            ],
        )

    def test_foreignkey_str_model_fields(self):
        lines = []
        name = "{}.{}.foreignkey_simple_model_str".format(
            SimpleModel2.__module__, SimpleModel2.__name__
        )
        obj = SimpleModel2.foreignkey_simple_model_str
        related_model = obj.field.remote_field.model
        obj.field.remote_field.model = "{}.{}".format(
            related_model.__module__, related_model.__name__
        )

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
                "**Model field:** foreignkey simple model str, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel` model.",
            ],
        )

    def test_reverse_foreignkey_model_fields(self):
        lines = []
        name = "{}.{}.reverse_foreignkey_simple_model".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.reverse_foreignkey_simple_model

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
                "**Model field:** foreignkey simple model, accesses the M2M "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel2` model.",
            ],
        )

    def test_reverse_foreignkey_str_model_fields(self):
        lines = []
        name = "{}.{}.reverse_foreignkey_simple_model_str".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.reverse_foreignkey_simple_model_str
        related_model = obj.rel.related_model
        obj.rel.related_model = "{}.{}".format(
            related_model.__module__, related_model.__name__
        )

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
                "**Model field:** foreignkey simple model str, accesses the M2M "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel2` model.",
            ],
        )

    def test_reverse_onetoone_model_fields(self):
        lines = []
        name = "{}.{}.reverse_onetoonefield".format(
            FileModel.__module__, FileModel.__name__
        )
        obj = FileModel.reverse_onetoonefield

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
                "**Model field:** onetoonefield, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel` model.",
            ],
        )

    def test_reverse_onetoone_str_model_fields(self):
        lines = []
        name = "{}.{}.reverse_onetoonefield_str".format(
            FileModel.__module__, FileModel.__name__
        )
        obj = FileModel.reverse_onetoonefield_str
        related_model = obj.related.related_model
        obj.related.related_model = "{}.{}".format(
            related_model.__module__, related_model.__name__
        )

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
                "**Model field:** onetoonefield str, accesses the "
                ":class:`~sphinxcontrib_django2.tests.test_docstrings.SimpleModel` model.",
            ],
        )

    def test_model_manager_fields(self):
        lines = []
        name = "{}.{}.custom_objects".format(
            SimpleModel.__module__, SimpleModel.__name__
        )
        obj = SimpleModel.custom_objects

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
                "Django manager to access the ORM",
                "Use ``SimpleModel.objects.all()`` to fetch all objects.",
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
