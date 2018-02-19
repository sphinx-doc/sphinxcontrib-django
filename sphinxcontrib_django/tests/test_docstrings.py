import os

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.test import SimpleTestCase
from sphinx.application import Sphinx

import sphinxcontrib_django
from sphinxcontrib_django import docstrings


class User2(models.Model):
    pass


class SimpleModel(models.Model):
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    user2 = models.ForeignKey('User2', related_name='+', on_delete=models.CASCADE)
    user3 = models.ForeignKey('auth.User', related_name='+', on_delete=models.CASCADE)


class SimpleForm(forms.ModelForm):
    test1 = forms.CharField(label="Test1")
    test2 = forms.CharField()

    class Meta:
        model = SimpleModel
        fields = ('user', 'user2', 'user3')


class TestDocStrings(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDocStrings, cls).setUpClass()
        root = os.path.dirname(sphinxcontrib_django.__file__)
        confdir = os.path.join(os.path.dirname(__file__), 'testdocs')
        cls.app = Sphinx(
            srcdir=root,
            confdir=confdir,
            outdir=os.path.join(confdir, '_build'),
            doctreedir=root,
            buildername='html',
            freshenv=True
        )
        sphinxcontrib_django.setup(cls.app)

    def test_foreignkey_type(self):
        """Test how the foreignkeys are rendered."""
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user')), ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`")
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user2')), ":type user2: ForeignKey to :class:`~sphinxcontrib_django.tests.test_docstrings.User2`")
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user3')), ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`")

    def test_model_init_params(self):
        """Model __init__ gets all fields as params."""
        lines = []
        docstrings._add_model_fields_as_params(self.app, SimpleModel, lines)
        self.assertEqual(lines, [
            ':param id: Id',
            ':type id: AutoField',
            ':param user: User',
            ':type user: ForeignKey to :class:`~django.contrib.auth.models.User`',
            ':param user2: User2',
            ':type user2: ForeignKey to :class:`~sphinxcontrib_django.tests.test_docstrings.User2`',
            ':param user3: User3',
            ':type user3: ForeignKey to :class:`~django.contrib.auth.models.User`',
        ])

    def test_add_form_fields(self):
        """Form fields should be mentioned."""
        lines = []
        docstrings._add_form_fields(SimpleForm, lines)
        self.assertEqual(lines, [
            '**Form fields:**',
            '',
            '* ``user``: User (:class:`~django.forms.models.ModelChoiceField`)',
            '* ``user2``: User2 (:class:`~django.forms.models.ModelChoiceField`)',
            '* ``user3``: User3 (:class:`~django.forms.models.ModelChoiceField`)',
            '* ``test1``: Test1 (:class:`~django.forms.fields.CharField`)',
            '* ``test2``: Test2 (:class:`~django.forms.fields.CharField`)',
        ])
