from django.contrib.auth.models import User
from django.db import models
from django.test import SimpleTestCase

from sphinxcontrib_django import docstrings


class User2(models.Model):
    pass


class SimpleModel(models.Model):
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    user2 = models.ForeignKey('User2', related_name='+', on_delete=models.CASCADE)
    user3 = models.ForeignKey('auth.User', related_name='+', on_delete=models.CASCADE)


class TestDocStrings(SimpleTestCase):
    """Test how the foreignkeys are rendered."""

    def test_foreignkey_type(self):
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user')), ":type user: ForeignKey to :class:`~django.contrib.auth.models.User`")
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user2')), ":type user2: ForeignKey to :class:`~sphinxcontrib_django.tests.test_docstrings.User2`")
        self.assertEqual(docstrings._get_field_type(SimpleModel._meta.get_field('user3')), ":type user3: ForeignKey to :class:`~django.contrib.auth.models.User`")
