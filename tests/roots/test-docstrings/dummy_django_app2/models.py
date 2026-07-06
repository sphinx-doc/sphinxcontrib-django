from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class GenericRelationModel(models.Model):
    # specifically test deferred string-type argument
    relation_field = GenericRelation("dummy_django_app.TaggedItem")
